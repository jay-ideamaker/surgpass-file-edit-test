from django.shortcuts import render
import subprocess
import os
from uuid import uuid4

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup

from .models import Question
from .serializers import QuestionSerializer

# This is our main conversion logic
def process_docx_file(docx_file_obj, filename):
    # Create a unique directory for this file's media
    unique_id = uuid4().hex
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp', unique_id)
    os.makedirs(temp_dir, exist_ok=True)

    # Save the uploaded docx temporarily
    temp_docx_path = os.path.join(temp_dir, filename)
    with open(temp_docx_path, 'wb+') as f:
        for chunk in docx_file_obj.chunks():
            f.write(chunk)

    # 1. Convert DOCX to HTML with Pandoc
    media_dir = os.path.join(temp_dir, 'media')
    os.makedirs(media_dir, exist_ok=True)
    html_output_path = os.path.join(temp_dir, 'output.html')
    
    # This command preserves table styles by adding the +styles extension
    subprocess.run([
        'pandoc',
        '-f', 'docx',
        '-t', 'html+styles', # Use html+styles to keep inline styles
        temp_docx_path,
        '-o', html_output_path,
        f'--extract-media={media_dir}'
    ], check=True)

    # 2. Convert DOCX to PDF with LibreOffice for viewing
    pdf_output_dir = os.path.join(settings.MEDIA_ROOT, 'pdf')
    os.makedirs(pdf_output_dir, exist_ok=True)
    subprocess.run([
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', pdf_output_dir,
        temp_docx_path
    ], check=True)
    
    pdf_filename = os.path.splitext(filename)[0] + '.pdf'
    pdf_path = os.path.join(pdf_output_dir, pdf_filename)


    # 3. Process HTML to update image paths
    with open(html_output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    
    # Create a permanent media folder for this question
    permanent_media_dir = os.path.join(settings.MEDIA_ROOT, 'images', unique_id)
    os.makedirs(permanent_media_dir, exist_ok=True)

    for img in images:
        old_src = img['src']
        # old_src is like 'media/image1.png'
        old_image_path = os.path.join(media_dir, old_src)
        new_image_name = os.path.basename(old_image_path)
        
        # Move image to permanent location
        permanent_image_path = os.path.join(permanent_media_dir, new_image_name)
        os.rename(old_image_path, permanent_image_path)

        # Update src to a public URL
        img['src'] = os.path.join(settings.MEDIA_URL, 'images', unique_id, new_image_name)

    return str(soup), pdf_path


class QuestionListCreateView(APIView):
    def get(self, request):
        questions = Question.objects.all().order_by('created_at')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response(
                {"error": "File not provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            html_content, pdf_path = process_docx_file(file_obj, file_obj.name)
            
            # Save the original docx file
            docx_save_path = os.path.join('docx', f"{uuid4().hex}_{file_obj.name}")
            with open(os.path.join(settings.MEDIA_ROOT, docx_save_path), 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

            question = Question.objects.create(
                original_filename=file_obj.name,
                html_content=html_content,
                docx_file=docx_save_path,
                pdf_file=pdf_path.replace(settings.MEDIA_ROOT + '/', '')
            )
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class QuestionDetailView(APIView):
    def delete(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            # You might want to delete the associated files from media too
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            question = Question.objects.get(pk=pk)
            question.html_content = request.data.get('html_content', question.html_content)
            question.save()
            serializer = QuestionSerializer(question)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
def process_docx_file(docx_file_path, original_filename):
    # The file is already saved, so we don't need to write it again.
    # We just need a unique directory for the output media.
    unique_id = uuid4().hex
    # We can use the directory of the docx file as a base for temp output
    temp_output_dir = os.path.join(os.path.dirname(docx_file_path), 'temp_media', unique_id)
    os.makedirs(temp_output_dir, exist_ok=True)

    # 1. Convert DOCX to HTML with Pandoc
    media_dir = os.path.join(temp_output_dir, 'media')
    os.makedirs(media_dir, exist_ok=True)
    html_output_path = os.path.join(temp_output_dir, 'output.html')
    
    subprocess.run([
        'pandoc',
        '-f', 'docx',
        '-t', 'html',
        docx_file_path, # Use the provided path
        '-o', html_output_path,
        f'--extract-media={media_dir}'
    ], capture_output=True, text=True, check=True)

    # 2. Convert DOCX to PDF with LibreOffice for viewing
    pdf_output_dir = os.path.join(settings.MEDIA_ROOT, 'pdf')
    os.makedirs(pdf_output_dir, exist_ok=True)
    subprocess.run([
        'libreoffice',
        '--headless',
        '--convert-to', 'pdf',
        '--outdir', pdf_output_dir,
        docx_file_path # Use the provided path
    ], check=True)
    
    pdf_filename = os.path.splitext(original_filename)[0] + '.pdf'
    pdf_path = os.path.join(pdf_output_dir, pdf_filename)

    # 3. Process HTML (this part remains the same)
    with open(html_output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    
    permanent_media_dir = os.path.join(settings.MEDIA_ROOT, 'images', unique_id)
    os.makedirs(permanent_media_dir, exist_ok=True)

    api_base_url = "https://surgpass-api.logicadev.top"

    for img in images:
        old_src = img['src']
        old_image_path = os.path.join(media_dir, old_src)
        new_image_name = os.path.basename(old_image_path)
        
        permanent_image_path = os.path.join(permanent_media_dir, new_image_name)
        os.rename(old_image_path, permanent_image_path)

        # --- MODIFIED: Build the full, absolute URL ---
        relative_url = os.path.join(settings.MEDIA_URL, 'images', unique_id, new_image_name)
        img['src'] = api_base_url + relative_url

    return str(soup), pdf_path


class QuestionListCreateView(APIView):
    def get(self, request):
        questions = Question.objects.all().order_by('created_at')
        serializer = QuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response(
                {"error": "File not provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 1. Define the permanent path and save the file immediately.
            docx_filename = f"{uuid4().hex}_{file_obj.name}"
            docx_dir = os.path.join(settings.MEDIA_ROOT, 'docx')
            os.makedirs(docx_dir, exist_ok=True)
            permanent_docx_path = os.path.join(docx_dir, docx_filename)

            with open(permanent_docx_path, 'wb+') as destination:
                for chunk in file_obj.chunks():
                    destination.write(chunk)

            # 2. Pass the PATH to the processing function, not the file object.
            html_content, pdf_path = process_docx_file(permanent_docx_path, file_obj.name)
            
            # 3. Create the Question object with the final paths.
            question = Question.objects.create(
                original_filename=file_obj.name,
                html_content=html_content,
                docx_file=os.path.join('docx', docx_filename), # Relative path for the model
                pdf_file=pdf_path.replace(settings.MEDIA_ROOT + '/', '')
            )
            serializer = QuestionSerializer(question, context={'request': request})
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
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

from rest_framework import serializers
from .models import Question

class QuestionSerializer(serializers.ModelSerializer):
    # Make file fields return the full URL
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'id', 
            'original_filename', 
            'html_content', 
            'pdf_url',
            'created_at'
        ]
    
    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if obj.pdf_file and hasattr(obj.pdf_file, 'url'):
            return request.build_absolute_uri(obj.pdf_file.url)
        return None
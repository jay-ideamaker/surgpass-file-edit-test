from django.db import models

class Question(models.Model):
    # The original docx file name
    original_filename = models.CharField(max_length=255)
    # The converted HTML content we will edit
    html_content = models.TextField()
    # Path to the original docx file for re-processing if needed
    docx_file = models.FileField(upload_to='docx/')
    # Path to the generated PDF for viewing
    pdf_file = models.FileField(upload_to='pdf/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_filename

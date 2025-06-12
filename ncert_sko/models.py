from django.db import models
from django.utils import timezone

class StudentClass(models.Model):
    class_name = models.CharField(max_length=50)
    class_value = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = ('Class')
        verbose_name_plural = ('Class')

class Subject(models.Model):
    subject_name = models.CharField(max_length=100) 
    class_name = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return f"{self.class_name.class_name} {self.subject_name}"

    class Meta:
        verbose_name = ('Subject')
        verbose_name_plural = ('Subject')

class ContentType(models.Model):
    content_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.content_type

    class Meta:
        verbose_name = ('ContentType')
        verbose_name_plural = ('ContentType')

def upload_to_dynamic_path(instance, filename):
    """
    Custom function to dynamically generate the file upload path based on class and subject.
    """
    # Get the class name and subject name
    class_name = instance.subject.class_name.class_name.replace(" ", "")
    subject_name = instance.subject.subject_name.replace(" ", "")
    
    # Construct the folder structure
    return f'pdf/ncert/{class_name}/{subject_name}/{filename}'

class PdfLinks(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="contents")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="contents")
    content_name = models.CharField(max_length=500, blank=True, null=True) 
    action_url = models.FileField(upload_to=upload_to_dynamic_path, blank=True, null=True) 

    def __str__(self):
        return f"{self.subject} - {self.action_url}"

    class Meta:
        verbose_name = ('PDFLinks')
        verbose_name_plural = ('PDFLinks')


class PdfDownloadTracker(models.Model):
    user_id = models.CharField(max_length=100) 
    email = models.EmailField(max_length=150, null=True, blank=True)  
    pdf_link = models.ForeignKey(PdfLinks, on_delete=models.CASCADE, related_name="downloads")
    timestamp = models.DateTimeField(default=timezone.now)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id}-{self.pdf_link.content_name}"

    class Meta:
        verbose_name = 'PDFDownload Tracker'
        verbose_name_plural = 'PDFDownload Tracker'
from django.db import models

# Create your models here.
class ProgramDetails(models.Model):
    program_name = models.CharField(max_length=255)
    slug = models.CharField(blank=True, null=True,max_length=120)
    

    def __str__(self):
        return self.program_name

    class Meta:
        app_label = "common_models"
        verbose_name = ('Program Details')
        verbose_name_plural = ('Program Details')


class CourseDetails(models.Model):
    course_name = models.CharField(max_length=255)
    course_id = models.CharField(blank=True, null=True,max_length=60)
    

    def __str__(self):
        return self.course_name

    class Meta:
        app_label = "common_models"
        verbose_name = ('Course Details')
        verbose_name_plural = ('Course Details')
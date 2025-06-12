from django.contrib import admin
from .models import ProgramDetails, CourseDetails
import uuid
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin
from import_export import fields

# Register your models here.

class ProgramDetailsAdmin(ImportExportActionModelAdmin):
    list_display = ['program_name','slug']

admin.site.register(ProgramDetails,ProgramDetailsAdmin)

class CourseDetailsAdmin(ImportExportActionModelAdmin):
    list_display = ['course_name','course_id']

admin.site.register(CourseDetails,CourseDetailsAdmin)
from django.contrib import admin
from .models import StudentClass, Subject, ContentType, PdfLinks, PdfDownloadTracker
from import_export.admin import ImportExportActionModelAdmin
from django.utils.text import slugify


class StudentClassAdmin(admin.ModelAdmin):
    list_display=['id','class_name','class_value']


class SubjectAdmin(ImportExportActionModelAdmin):
    list_display=['subject_name','class_name']

class ContentTypeAdmin(admin.ModelAdmin):
    list_display=['content_type']

class PdfLinksAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'content_name', 'action_url']

# class PdfLinksAdmin(admin.ModelAdmin):
#     list_display = ['id', 'subject', 'content_name', 'dynamic_folder_path']

    # Method to display dynamic folder structure in admin panel
    # def dynamic_folder_path(self, obj):
    #     class_name = slugify(obj.subject.class_name.class_name)
    #     subject_name = slugify(obj.subject.subject_name)
    #     filename = obj.action_url.name.split('/')[-1]
    #     return f"pdf/ncert/{class_name}/{subject_name}/{filename}"

    # dynamic_folder_path.short_description = "Dynamic Folder Path"

class PdfDownloadTrackerAdmin(ImportExportActionModelAdmin):
    list_display = ['id','user_id','email','pdf_link','timestamp','downloaded']






admin.site.register(StudentClass, StudentClassAdmin)
admin.site.register(Subject,SubjectAdmin)
admin.site.register(ContentType,ContentTypeAdmin)
admin.site.register(PdfLinks,PdfLinksAdmin)
admin.site.register(PdfDownloadTracker,PdfDownloadTrackerAdmin)
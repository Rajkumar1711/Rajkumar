# admin.py
from django.contrib import admin

from import_export.results import Error, Result
from import_export import fields, resources
from import_export.admin import ImportExportActionModelAdmin
from ibm_tnsdc3.models import College, Project, User, Team, TnsdcEnrollment, TnsdcSubmission
from import_export.widgets import ForeignKeyWidget,ManyToManyWidget
from django import forms


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_name", "mentor", "members", "project"]

class PermissiveForeignKeyWidget(ForeignKeyWidget):
    def clean(self, value, row=None, **kwargs):
        try:
            return super().clean(value)
        except self.model.DoesNotExist:
            return value


class UserResource(resources.ModelResource):
    college = fields.Field(
        column_name='college',
        attribute='college',
        widget=ForeignKeyWidget(College, 'college_name')
    )
    
    class Meta:
        model = User
    ''' 
    def skip_row(self, instance, original, row, import_validation_errors=None):
        try:
            email = User.objects.get(email=row["email"])
        except:
            email = None
        if(email):
            return True # Duplicate email
        else:
            email = row["email"]
            print("Skipping")
            return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)
            #return True
    '''
class ProjectResource(resources.ModelResource):
    college = fields.Field(
        column_name='college',
        attribute='college',
        widget=ManyToManyWidget(College, field='college_name')
    )

    
    class Meta:
        model = Project


@admin.register(College)
class CollegeAdmin(ImportExportActionModelAdmin):
    list_display = ["id", "college_id", "college_name","course_id","team_size"]
    search_fields = ["college_name"]

@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin):
    resource_class = ProjectResource
    list_display = [ "project_name","course_id", "course_name","get_college"]
    list_filter = [ "course_name","college"]
    search_fields = ["project_name", "course_id", "course_name"]

@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource
    list_display = ["id", "nm_id", "email", "first_name", "last_name", "role", "college","course_id","batch","year","is_evaluator"]
    list_filter = ["role","course_id"]
    search_fields = ["email", "first_name", "last_name","college__college_name", "role"] 
    import_export_change_list_template = 'admin/import_export/change_list_import_export.html'

class TeamResource(resources.ModelResource):
    project = fields.Field(column_name='project', attribute='project',widget=ForeignKeyWidget(Project, 'project_name'))
    mentor = fields.Field(
        column_name='mentor',
        attribute='mentor',
        widget=ForeignKeyWidget(User, 'email')
    )
    members = fields.Field(column_name='members', attribute='get_members')
    evaluator =  fields.Field(
        column_name='evaluator',
        attribute='evaluator',
        widget=ForeignKeyWidget(User, 'email')
    )

    class Meta:
        model = Team
        fields = ('id', 'team_name', 'project', 'mentor', 'members','evaluator')

@admin.register(Team)
class TeamAdmin(ImportExportActionModelAdmin):
    resource_class = TeamResource
    list_display = ["id", "team_name","project", "mentor","get_members","evaluator"]
    list_filter = ["mentor","team_name","project"]
    search_fields = ["team_name", "mentor_email","", "project_project_name"]


class TnsdcEnrollmentResource(resources.ModelResource):
    email = fields.Field(
        column_name='email',
        attribute='email',
        widget=PermissiveForeignKeyWidget(User, 'email')
    )
    class Meta:
        model = TnsdcEnrollment
        fields = ('id', 'course_id', 'email', 'is_enrolled','is_registered')
    def skip_row(self, instance, original, row, import_validation_errors=None):
        if "email" in import_validation_errors  and len(import_validation_errors["email"]) > 0:
            import_validation_errors["email"] = row["email"]
            return True
        return False
@admin.register(TnsdcEnrollment)
class TnsdcEnrollmentAdmin(ImportExportActionModelAdmin):
    resource_class = TnsdcEnrollmentResource
    list_display = ["id", "course_id","email", "is_enrolled","is_registered"]
    list_filter = ["course_id"]
    search_fields = ["course_id", "email__email"]

class TnsdcSubmissionResource(resources.ModelResource):
    email = fields.Field(
        column_name='email',
        attribute='email',
        widget=ForeignKeyWidget(User, 'email')
    )
    college = fields.Field(
        column_name='college',
        attribute='college',
        widget=ForeignKeyWidget(College, 'college_name')
    )
    team_name = fields.Field(
        column_name='team_name',
        attribute='team_name',
        widget=ForeignKeyWidget(Team, 'team_name')
    )

    class Meta:
        model = TnsdcSubmission


@admin.register(TnsdcSubmission)
class TnsdcSubmissionAdmin(ImportExportActionModelAdmin):
    resource_class = TnsdcSubmissionResource
    list_display = ["id","email","college","team_name","course_id", "phase1_submitted","eval_a1","eval_a2","avg1"]
    list_filter = ["college"]
    search_fields = ["email", "college","team_name"]
    # search_fields = ['email__email']
    
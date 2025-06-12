# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ibm_tnsdc.models import College, Project, User, Team,TeamMembers
from import_export import fields, resources
from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import ForeignKeyWidget


class UserResource(resources.ModelResource):
    college = fields.Field(
        column_name='college',
        attribute='college',
        widget=ForeignKeyWidget(College, 'college_name')
    )
    
    class Meta:
        model = User


class ProjectResource(resources.ModelResource):
    college = fields.Field(
        column_name='college',
        attribute='college',
        widget=ForeignKeyWidget(College, 'college_name')
    )
  
    class Meta:
        model = Project

class TeamResource(resources.ModelResource):
    project = fields.Field(
        column_name='project',
        attribute='project',
        widget=ForeignKeyWidget(Project, 'project_name')
    )
  
    class Meta:
        model = Team

# class TeamMembersResource(resources.ModelResource):
#     # user = fields.Field(
#     #     column_name='user',
#     #     attribute='user',
#     #     widget=ForeignKeyWidget(User, 'first_name')
#     # )

#     team = fields.Field(
#         column_name='team',
#         attribute='team',
#         widget=ForeignKeyWidget(Team, 'team_name')
#     )
  
#     class Meta:
#         model = TeamMembers



@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource
    list_display = ['email','first_name','last_name','role','course_id','college']
    list_filter = ('email',)


    
@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin):
    resource_class = ProjectResource
    list_display = ['project_name','project_description','course_id','course_name','college']
    list_filter = ('project_name','course_id','course_name',)



@admin.register(College)
class CollegeAdmin(ImportExportActionModelAdmin):
    list_display = ["college_name","team_size"]
    list_filter = ('college_name',) 
    
@admin.register(Team)
class TeamAdmin(ImportExportActionModelAdmin):
    resource_class = TeamResource
    list_display = ["team_name","project"]
    list_filter = ('team_name',)

@admin.register(TeamMembers)
class TeamMembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'team']
    list_filter = ['team']
    readonly_fields = ['project'] # this is the readonly field
    fields = [ 'user', 'team', 'project']

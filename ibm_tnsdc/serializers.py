# serializers.py
from rest_framework import serializers
from ibm_tnsdc.models import *

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = ['id', 'college_name','team_size']

class ProjectSerializer(serializers.ModelSerializer):
    college = serializers.SlugRelatedField(slug_field='college_name', queryset=College.objects.all())
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_description', 'course_id', 'course_name', 'college']

class UserSerializer(serializers.ModelSerializer):
    college_id = serializers.IntegerField(source='college.id')
    college = serializers.SlugRelatedField(slug_field='college_name', queryset=College.objects.all())
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role','course_id','college_id','college']

class TeamSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='project_name', queryset=Project.objects.all())
    class Meta:
        model = Team
        fields = ['id', 'team_name', 'project']


class TeamMembersSerializer(serializers.ModelSerializer):
    user = serializers.EmailField(source='user.email')
    team = serializers.CharField(source='team.team_name')
    project_id = serializers.IntegerField(source='project.id',required=False)
    project_name = serializers.CharField(source='project.project_name',required=False)
    course_id = serializers.CharField(source='project.course_id',required=False)
    course_name = serializers.CharField(source='project.course_name',required=False)

    class Meta:
        model = TeamMembers
        fields = ['id', 'user', 'team', 'project_id', 'project_name', 'course_id', 'course_name']

    def update(self, instance, validated_data):
        # get the user and team from the validated data
        user_email = validated_data.get('user').get('email')
        team_name = validated_data.get('team').get('team_name')

        # get the corresponding User and Team objects from the database
        user = User.objects.get(email=user_email)
        team = Team.objects.get(team_name=team_name)

        # update the instance with the new user and team
        instance.user = user
        instance.team = team
        instance.save()

        return instance

    def create(self, validated_data):
        # get the user and team from the validated data
        user_email = validated_data.get('user').get('email')
        team_name = validated_data.get('team').get('team_name')

        # get the corresponding User and Team objects from the database
        user = User.objects.get(email=user_email)
        team = Team.objects.get(team_name=team_name)

        # create a new TeamMembers object with the user and team
        instance = TeamMembers.objects.create(user=user, team=team)

        return instance



    





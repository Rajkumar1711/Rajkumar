# serializers.py
from rest_framework import serializers
from ibm_tnsdc3.models import User,Project,College,Team



class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id","project_name", "project_description", "course_id", "course_name", "college"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","email", "first_name", "last_name", "role", "college","course_id","branch","technology"]
        
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name= (validated_data.get('last_name', instance.last_name))
    #     instance.branch = validated_data.get('branch', instance.branch)
    #     instance.technology= (validated_data.get('technology', instance.technology))
    #     instance.role= (validated_data.get('role', instance.role))
    #     instance.save()
    #     return instance

class TeamSerializer(serializers.ModelSerializer):
    mentor = serializers.SlugRelatedField(slug_field="email", queryset=User.objects.all())
    members = serializers.SlugRelatedField(slug_field="email", many=True, queryset=User.objects.all(),required=False)
    project = serializers.SlugRelatedField(slug_field="project_name", queryset=Project.objects.all())
    class Meta:
        model = Team
        fields = ["id","team_name", "mentor", "members", "project"]

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.mentor = validated_data.get('mentor', instance.mentor)
        instance.members.set(validated_data.get('members', instance.members.all()))
        instance.save()
        return instance
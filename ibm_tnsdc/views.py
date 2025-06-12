from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from ibm_tnsdc.models import *
from .serializers import *
from collections import defaultdict


import logging
log = logging.getLogger(__name__)

# views.py

class AllCollegesApiView(APIView):

    def get(self,request):
        college_name = request.query_params.get('college_name')
        if college_name:
            colleges = College.objects.filter(college_name=college_name)
        else:
            colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AllUsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserAPIView(APIView):
    """
    View to list, create and update users based on email id.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get the email id from the query params or return 400 if not provided
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Get the user object with the given email or return 404 if not found
        user = get_object_or_404(User, email=email)
        # Serialize the user object
        serializer = UserSerializer(user)
        # Return the serialized data as a response
        return Response(serializer.data)


    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, format=None):
        # Get the email id from the query params or return 400 if not provided
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'email is required'}, status=status.HTTP_400_BAD_REQUEST)
        # Get the user object with the given email or return 404 if not found
        user = get_object_or_404(User, email=email)
        # Deserialize the request data with the existing user object as an instance
        serializer = UserSerializer(user, data=request.data)
        # Validate the data and update the user object
        if serializer.is_valid():
            # Use validated_data instead of request.data
            user.email = serializer.validated_data['email']
            user.first_name = serializer.validated_data['first_name']
            user.last_name = serializer.validated_data['last_name']
            user.role = serializer.validated_data['role']
            user.college = serializer.validated_data['college']
            user.save()
            # Return the serialized data as a response
            return Response(serializer.data)
        # Return the validation errors and a 400 status code
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
class AllTeamsAPIView(APIView):
    
    def get(self,request):
        id = request.query_params.get('team_id')
        if id:
            teams = Team.objects.filter(id=id)
        else:
            teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def post(self,request):
        # create a new team
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        # update an existing team
        id = request.query_params.get('team_id')
        if id:
            team = Team.objects.get(id=id)
            serializer = TeamSerializer(team, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "team_id is required"}, status=status.HTTP_400_BAD_REQUEST)




class NewTeamMembersAPIView(APIView):
    """
    View to list, create and update TeamMembers based on id
    """
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        id = self.request.query_params.get('member_id')
        member = None
        if id is not None:
            try:
                member = TeamMembers.objects.get(id=id)
            except TeamMembers.DoesNotExist:
                member = None
        return member


    def get(self, request, format=None):
        member = self.get_object()
        if member is not None:
            serializer = TeamMembersSerializer(member)
            return Response(serializer.data)
        else:
            return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)


    def put(self, request, format=None):
        member = self.get_object()
        if member is not None:
            serializer = TeamMembersSerializer(member, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = TeamMembersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class TeamMembersList(APIView):
    def get(self, request, format=None):
        # filter the team members by the project id
        team = request.query_params.get('project_id')
        team_members = TeamMembers.objects.filter(team=team)
        # serialize the team members using the serializer class
        serializer = TeamMembersSerializer(team_members, many=True)
        # return the serialized data as a response
        return Response({"team_members": serializer.data})


class AllProjectsAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectAPIView(APIView):
    """
    View to list, create and update projects based on course_id&college_id.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.request.query_params.get('course_id')
        college_id = self.request.query_params.get('college_id')
        project = None
        if course_id is not None and college_id is not None:
            try:
                project = Project.objects.filter(course_id=course_id, college_id=college_id)
            except Project.DoesNotExist:
                project = None
        return project


    def get(self, request, format=None):
        project = self.get_object()
        if project is not None:
            data = []
            grouped_projects = defaultdict(list) # create a dictionary to store the grouped projects
            for p in project:
                serializer = ProjectSerializer(p)
                project_data = serializer.data
                # use a tuple of course_id, course_name and college as the key
                key = (project_data['course_id'], project_data['course_name'], project_data['college'])
                # create a nested dictionary with the remaining fields
                value = {'id': project_data['id'], 'project_name': project_data['project_name'], 'project_description': project_data['project_description']}
                # append the value to the list of projects under the same key
                grouped_projects[key].append(value)
                
                # query the TeamMembers model for the current project
                # team_members = TeamMembers.objects.filter(project=p).values('id', 'user__email', 'team_name', 'project__id', 'project__project_name', 'project__course_id', 'project__course_name')
                team_members = TeamMembers.objects.filter(team__project=p).values('id', 'user', 'team', 'team_id', 'user_id')
                num_records = len(team_members)
                team_size = 5
                seats_filled = num_records
                seats_available = team_size - seats_filled
                
                # add the team information to the value dictionary
                value['team_size'] = team_size
                value['seats_filled'] = seats_filled
                value['seats_available'] = seats_available
                
            # convert the grouped projects to the desired format
            for key, value in grouped_projects.items():
                # create a dictionary with the key fields and the list of projects as values
                item = {'course_id': key[0], 'course_name': key[1], 'college': key[2], 'projects': value}
                data.append(item)
            return Response(data)
        else:
            return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)



    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        project = self.get_object()
        if project is not None:
            serializer = ProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Record not found'},status=status.HTTP_404_NOT_FOUND)


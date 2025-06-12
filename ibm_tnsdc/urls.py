from django.conf import settings
from django.urls import path
# from .views import *
from .views import *


urlpatterns = [
    path('colleges-info/', AllCollegesApiView.as_view(), name='colleges-api'),  # ?college_name=
    path('users-info/', AllUsersAPIView.as_view(), name='users-api'),           # nothing to pass
    path('projects-info/', AllProjectsAPIView.as_view(), name='projects-api'),  # nothing to pass
    path('all-teams-info/', AllTeamsAPIView.as_view(), name='teams-api'),       # ?team_id (GET,POST,PUT)

    
    path('user/', UserAPIView.as_view()),                     # ?email=      (GET,POST,PUT)
    path('project/', ProjectAPIView.as_view()),               # ?course_id=&college_id=   (GET,POST,PUT)
    path('teams/', TeamMembersList.as_view()),                # ?project_id=  (GET only)
    path('team-member/', NewTeamMembersAPIView.as_view()),    # ?member_id= (GET,PUT,POST)
 
]















# urlpatterns = [
#     path('user-api/', UserAPIView.as_view(), name='user-api1'),
#     path('user-api/<str:email>/', UserAPIView.as_view(), name='user-api2'),
# ]


# urlpatterns = [

#     path('users/', UserDetail.as_view()),
# ]
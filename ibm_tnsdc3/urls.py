from django.conf import settings
from django.urls import path
from .views import *
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView
# )


urlpatterns = [
    path('team/', NewTeamMembersAPIView.as_view()),
    path('mentor/', MentorAPIView.as_view()), 
    path('spoc/', SpocAPIView.as_view(), name='spoc-p2'),
    path('overall-dashboard/', OverallDashboardAPIView.as_view()), 
    path('principal-dashboard/', PrincipalDashboardAPIView.as_view()),
    path('mentor-dashboard/', MentorDashboardAPIView.as_view()),
    path('admin-submissions/', PhasewiseSubmissionAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    # path('user/<str:token>/', UserAPIView.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]



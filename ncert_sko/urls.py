# from django.conf import settings
from django.urls import path
from .views import NcertDataView, NcertSubjectsView, TrackPdfDownloadAPIView, NcertClassesView
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('classes/', NcertClassesView.as_view(), name='classes'),
    path('subjects/', NcertSubjectsView.as_view(), name='subjects'),
    path('pdfdata_links/', NcertDataView.as_view(), name='pdf-links'), 
    path('track-pdfdownload/', TrackPdfDownloadAPIView.as_view(), name='track_pdf_download'),
]
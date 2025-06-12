"""
URL configuration for skocommon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ncert/', include('ncert_sko.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('ncert_sko/', include('ncert_sko.urls')),
#     # path('ibm/', include(('ibm_tnsdc.urls', 'ibm_tnsdc'), namespace='ibm_tnsdc'))
#     # path('ibm3/', include(('ibm_tnsdc3.urls', 'ibm_tnsdc3'), namespace='ibm_tnsdc3')),
#     # path('ncert_sko/', include(('ncert_sko.urls', 'ncert_sko'), namespace='ncert_sko')),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify')
# ]

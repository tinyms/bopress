"""BoPress URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from oauth2.views import WeXinApiView, UserInfoViewSet, CompanyInfoViewSet, CompanyInfoCreateView, \
    CompanyEmployeeViewSet, AppCommerceLicenseViewSet, AppGrantAuthorizationViewSet

from train.views import CourseViewSet, TeacherViewSet, StudentViewSet, EnrollViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'api/v1/userinfo', UserInfoViewSet)
router.register(r'api/v1/companyinfo', CompanyInfoViewSet)
router.register(r'api/v1/employees', CompanyEmployeeViewSet)
router.register(r'api/v1/license', AppCommerceLicenseViewSet)
router.register(r'api/v1/grant', AppGrantAuthorizationViewSet)
router.register(r'api/v1/train/teacher', TeacherViewSet)
router.register(r'api/v1/train/course', CourseViewSet)
router.register(r'api/v1/train/student', StudentViewSet)
router.register(r'api/v1/train/enroll', EnrollViewSet)

schema_view = get_schema_view(title='BoPress API')

urlpatterns = [
    url(r'^api/v1/oauth2/$', WeXinApiView.as_view()),
    url(r'^api/v1/companyinfocreate/$', CompanyInfoCreateView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api/schema/$', schema_view),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
]

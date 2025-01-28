"""healthbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import re_path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from api.views import MyTokenObtainPair,registration
from healthmanage.views import index

schema_view = get_schema_view(
    openapi.Info(
        title="健康管理接口文档平台",  
        default_version="v1",  
        description="健康管理接口描述",  
        terms_of_service="",  
        contact=openapi.Contact(email="wys@qq.com"),  
        license=openapi.License(name="Apache License 2.0")  
    ),
    public=True,  
    permission_classes=(permissions.AllowAny,) 
)

urlpatterns = [
    #re_path('', index, name='index'),
    re_path('admin/', admin.site.urls),
    re_path("api/swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger"),  
    re_path("api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"), 
    # 自定义登录注册
    re_path('register/', registration, name='register'),

    re_path('healthmanage/', include('healthmanage.urls')),
    re_path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

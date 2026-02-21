"""
URL configuration for dormfix_backend project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from repairs.views import serve_db_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/repairs/', include('repairs.urls')),
    path('api/', include('announcements.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # 上传文件存数据库，通过此视图从 DB 读出并返回
    path('media/db/<int:pk>/', serve_db_file, name='serve_db_file'),
]

# 开发环境下静态文件
if settings.DEBUG and getattr(settings, 'STATIC_ROOT', None):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

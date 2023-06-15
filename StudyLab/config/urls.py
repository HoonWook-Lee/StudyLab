"""
URL configuration for config project.

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

# View 함수
from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # 메인 화면
    path('', index, name='index'),

    # 사용자 관련 화면
    path('user/', include('core.user.urls')),

    # 키워드 관련 화면
    path('keyword/', include('core.keyword.urls')),

    # 메모 관련 화면
    path('memo/', include('core.memo.urls')),

    # 검색 관련 화면
    path('search/', include('core.search.urls')),
]

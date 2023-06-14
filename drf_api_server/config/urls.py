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

# static 파일
from django.urls import re_path as url
from django.views.static import serve
from django.conf import settings

# Token
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

# rest_framework
from rest_framework import routers
from core.keyword.apis import KeywordViewSet
from core.memo.apis import MemoViewSet

# router 지정
router = routers.DefaultRouter()
router.register(r'keywords', KeywordViewSet)
router.register(r'memos', MemoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    # 메인 화면 = docs
    path('', index, name='index'),

    # rest_framework
    path('apis/', include(router.urls)),

    # Token 발급 API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Uvicorn 에서 static, media 파일 불러오기 (UI 미사용 시 제거 가능, media는 파일 따로 관리 시 제거 가능)
    url(r'^static/(?P<path>.*)$', serve, {'document_root' : settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
]

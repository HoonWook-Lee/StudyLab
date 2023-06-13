from django.urls import path
from core.keyword.views import *

urlpatterns = [
    # 키워드 작성
    path('write', keyword_create, name='k-write'),
]
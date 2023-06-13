from django.urls import path
from core.keyword.views import *

urlpatterns = [
    # 키워드 작성
    path('write', keyword_create, name='k-write'),

    # 키워드 리스트
    path('list', keyword_list, name='k-list'),
]
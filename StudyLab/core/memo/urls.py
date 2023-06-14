from django.urls import path
from core.memo.views import *

urlpatterns = [
    # 메모 작성
    path('write', memo_create, name='m-write'),
]
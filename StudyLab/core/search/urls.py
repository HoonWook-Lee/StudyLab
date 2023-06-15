from django.urls import path
from core.search.views import *


urlpatterns = [
    # 책 검색하기
    path('book', book_search, name='b-search'),
]
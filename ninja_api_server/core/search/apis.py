from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.http.response import JsonResponse
from math import ceil
from core.search.book_func import *

router = Router()


@router.get('/books', tags=['검색 API 모음'], summary='도서 검색 API', auth=JWTAuth())
async def search_book(request, keyword : str, page : int = 1):
    """
    # 쿼리 파라미터 정보
    ## &emsp; keyword : 검색 키워드 정보(필수), page : 검색 페이지 정보
    """
    
    # 책 정보 가져오기
    books = await search_book_func(keyword, page)
    
    res = (lambda bsc : 
        dict(end_page=ceil(books.json()['total']/9), items=books.json()['items']) if bsc == 200 else books.json()
    )(books.status_code)

    return JsonResponse(res, status=books.status_code, safe=False)
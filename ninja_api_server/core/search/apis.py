from ninja import Router
from ninja_jwt.authentication import JWTAuth
from ninja.pagination import paginate, PageNumberPagination
from django.http.response import JsonResponse
from math import ceil
from aiohttp import ClientSession
from asyncio import gather
from typing import List
from core.search.book_func import *
from core.producer import publish
from core.search.schemas import BookSchema


router = Router()


@router.get('/books', tags=['검색 API 모음'], summary='도서 검색 API', auth=JWTAuth())
async def search_book(request, keyword : str, page : int = 1):
    """
    # 쿼리 파라미터 정보
    ## &emsp; keyword : 검색 키워드 정보(필수), page : 검색 페이지 정보
    """
    
    # 책 정보 가져오기
    books = await search_book_func(keyword, page)

    max_json = (lambda total : 112 if total > 1000 else ceil(books.json()['total']/9))(books.json()['total'])
    
    res = (lambda bsc : 
        dict(end_page=max_json, items=books.json()['items']) if bsc == 200 else books.json()
    )(books.status_code)

    return JsonResponse(res, status=books.status_code, safe=False)

@router.get('/crawling', tags=['검색 API 모음'], summary='도서 크롤링 API', auth=JWTAuth())
async def crawling_book(request):
    """
    # 비제이퍼블릭 홈페이지 크롤링 API 입니다.
    """

    res = {'message' : '최신 데이터 입니다.'}

    # 데이터가 없거나 1주일 주기로 최신화
    if await crawling_check_func():

        # 데이터 수집 메시지 저장
        await crawling_message_func(False)

        # 마지막 페이지 정보
        end_page = await crawling_end_func(env('BASE_URL'))

        # 정보를 가지고 온 경우
        if end_page != 0:
            # 모든 urls 모음
            urls = [f'{env("BASE_URL")}?page={i}' for i in range(1, int(end_page)+1)]

            # 비동기 수집
            async with ClientSession() as session:
                data_list = await gather(*[crawling_book_func(session, url, i) for i, url in enumerate(urls)])
            
            res_json = dict(items=data_list)

            # RabbitMQ 데이터 전송
            publish('데이터 최신화 완료', res_json)

            # 데이터 수집 메시지 저장
            await crawling_message_func(True)

            res = {'message' : '데이터 최신화 완료'}

    return JsonResponse(res, status=200, safe=False)

@router.get('/crawling-books', tags=['검색 API 모음'], summary='수집한 도서 API', response=List[BookSchema], auth=JWTAuth())
@paginate(PageNumberPagination, page_size=9)
def crawling_books(request):

    return Crawling.objects.all()
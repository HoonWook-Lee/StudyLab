from django.shortcuts import render
from core.utils import check_token
from core.models import Crawling_message, Crawling


# 책 검색
def book_search(request):

    # sidebar active
    nav_check = 'sidebar_book'

    # nav
    ns = 'search_nav'

    # keyword 관련 책 검색
    key = request.GET.get('keyword', '코딩')

    # 페이지 구현
    page = int(request.GET.get('p', 1))

    # Token
    token = check_token(request)

    return render(request, 'search/book.html', {
        'nav_check': nav_check, 'key': key, 'page' : page, 'ns' : ns, 'token' : token 
    })

# 책 크롤링
def book_crawling(request):

    # sidebar active
    nav_check = 'sidebar_book'

    # nav
    ns = 'search_nav'

    # 페이지 구현
    page = int(request.GET.get('p', 1))

    # Token
    token = check_token(request)

    # Message
    if Crawling.check_data() == 0:
        message = '책 정보를 수집 중 입니다.'
    else:
        message = Crawling_message.objects.latest('created_at').message

    return render(request, 'search/crawling.html', {
        'nav_check': nav_check, 'page' : page, 'ns' : ns, 'token' : token, 'message' : message
    })
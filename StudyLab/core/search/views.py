from django.shortcuts import render
from core.utils import check_token


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
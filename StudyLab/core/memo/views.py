from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.memo.forms import MemoForm
from core.utils import check_token


# 메모 작성 = 로그인 시 페이지 접근 가능
@login_required
def memo_create(request):

    # sidebar active
    nav_check = 'sidebar_memo'

    # 메모 폼
    form = MemoForm()

    # Token
    token = check_token(request)

    return render(request, 'memo/create.html', {'nav_check' : nav_check, 'form' : form, 'token' : token})

# 메모 리스트 보기
def memo_list(request):

    # sidebar active
    nav_check = 'sidebar_memo'

    # 페이지 구현
    page = int(request.GET.get('p', 1))

    return render(request, 'memo/list.html', {'nav_check' : nav_check, 'page' : page})

# 메모 상세보기
def memo_view(request):

    # sidebar active
    nav_check = 'sidebar_memo'

    return render(request, 'memo/retrieve.html', {'nav_check' : nav_check})
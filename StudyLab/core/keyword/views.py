from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.keyword.forms import KeywordForm
from core.utils import check_token

# 키워드 작성 = 로그인 시 페이지 접근 가능
@login_required
def keyword_create(request):

    # sidebar active
    nav_check = 'sidebar_label'

    # 키워드 폼
    form = KeywordForm()

    # Token
    token = check_token(request)
            
    return render(request, 'keyword/create.html', {'form' : form, 'token' : token, 'nav_check' : nav_check})
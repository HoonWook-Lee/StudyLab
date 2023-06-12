from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http.response import JsonResponse
from core.user.forms import *
from core.user.func import *


# 회원가입
def register_view(request):

    # POST 요청 확인
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        res = (
            lambda f : f.save(f.cleaned_data) if f.is_valid() else ('올바르지 않은 데이터 입니다.', 'error', 422)
        )(form)

        return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)
    else:
        form = RegisterForm()

        return render(request, 'user/register.html', {'form' : form})

# 로그인
def login_view(request):

    form = LoginForm()

    return render(request, 'user/login.html', {'form' : form})

# 로그아웃
def logout_view(request):

    logout(request)

    return redirect('login')

# 아이디 중복 확인
def user_check(request):

    user_id = request.GET.get('user_id')

    res = user_check_func(user_id)

    return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)
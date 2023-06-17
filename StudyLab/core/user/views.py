from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
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

    # POST 요청 확인
    if request.method == 'POST':
        form = LoginForm(request.POST)
        res = (
            lambda f : f.login(request, f.cleaned_data) if f.is_valid() else ('올바르지 않은 데이터 입니다.', 'error', 422)
        )(form)

        return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)
    else:
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

# 비밀번호 초기화
def pw_reset(request):

    # POST 요청 확인
    if request.method == 'POST':
        form = ResetForm(request.POST)
        res = (
            lambda x : x.reset(x.cleaned_data) if x.is_valid() else ('올바르지 않은 데이터 입니다.', 'error', 422)
        )(form)

        return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)
    else:
        form = ResetForm()

        return render(request, 'user/reset.html', {'form' : form})
    
# 비밀번호 변경
@login_required
def pw_change(request):

    # 유저 확인
    user = Users.objects.get(pk=request.user.id)

    # POST 요청 확인
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        res = (
            lambda x : x.change(request, x.cleaned_data) if x.is_valid() else ('올바르지 않은 데이터 입니다.', 'error', 422)
        )(form)

        return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)
    else:
        form = ChangeForm()

        return render(request, 'user/change.html', {'form' : form, 'user_id' : user})
    
# 비밀번호 변경
@login_required
def user_withdrawal(request):

    # sidebar active
    nav_check = 'sidebar_main'

    # DELETE 요청 확인
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        res = (
            lambda x : x.delete(x.cleaned_data) if x.is_valid() else ('올바르지 않은 데이터 입니다.', 'error', 422)
        )(form)

        return JsonResponse(data=dict(msg=res[0], check=res[1]), status=res[2], safe=False)
    else:
        form = WithdrawalForm()

        return render(request, 'user/delete.html', {'nav_check' : nav_check, 'form' : form})
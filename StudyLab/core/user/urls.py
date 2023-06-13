from core.user.views import *
from django.urls import path


urlpatterns = [
    # 로그인
    path('login', login_view, name='login'),

    # 회원가입
    path('register', register_view, name='register'),

    # 로그아웃
    path('logout', logout_view, name='logout'),

    # 아이디 중복 확인
    path('check', user_check, name='user_check'),

    # 비밀번호 초기화
    path('reset', pw_reset, name='pw_reset'),

    # 비밀번호 변경
    path('change', pw_change, name='pw_change'),
]
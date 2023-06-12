from django import forms
from re import match as re_match
from argon2 import PasswordHasher, exceptions
from django.contrib.auth import login
from core.models import Users


# 회원가입 Form
class RegisterForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'user_id', 'class' : 'form-control', 'placeholder' : '아이디를 입력해주세요', 'autofocus' : 'autofocus'
    }))

    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'id' : 'password', 'class' : 'form-control', 'placeholder' : '비밀번호를 입력해주세요',
        'aria-describedby' : 'password', 'autocomplete' : 'off'
    }))

    check_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'id' : 'check_password', 'class' : 'form-control', 'placeholder' : '비밀번호를 한번 더 입력해주세요',
        'aria-describedby' : 'check_password', 'autocomplete' : 'off'
    }))

    hint = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'hint', 'class' : 'form-control', 'placeholder' : '비밀번호 답변 (꼭 기억해주세요)'
    }))

    check = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput(attrs={
        'id' : 'check', 'class' : 'form-control', 'value' : 'False'
    }))

    # 회원가입
    def save(self, data):
        # 6자 이상, 최소 하나의 문자, 숫자, 특수 문자를 포함한 문자
        pw = data.get('password')
        result = re_match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$', pw)

        # 가능 유무 확인
        if data.get('check') == 'False':
            res = ('아이디 중복 확인 체크 후 \n 다시 시도하여 주세요.', 'error', 422)
        elif result is None:
            res = ('비밀번호는 반드시 하나 이상의 \n 영문자, 숫자, 특수 문자를 포함한 \n 6자리 이상 조합이여야 합니다.', 'error', 422)
        elif pw != data.get('check_password'):
            res = ('비밀번호가 일치하지 않습니다.', 'error', 422)
        else:
            # 회원 가입
            user = Users(
                username = data.get('user_id'), 
                password = 'argon2' + PasswordHasher().hash(pw), # PasswordHasher와 Django Argon2의 차이 제거
                hint = data.get('hint')
            )
            user.save()
            
            res = ('회원 가입이 완료되었습니다.', 'success',  200)

        return res


# 로그인 Form
class LoginForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'user_id', 'class' : 'form-control', 'placeholder' : '아이디를 입력해주세요', 'autofocus' : 'autofocus'
    }))

    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'id' : 'password', 'class' : 'form-control', 'placeholder' : '비밀번호를 입력해주세요',
        'aria-describedby' : 'password', 'autocomplete' : 'off'
    }))

    # 로그인
    def login(self, request, data):
        
        res = ('올바른 유저ID와 패스워드를 \n 입력하여 주세요.', 'error', 422)

        user_id = data.get('user_id')

        try:
            # 등록 정보 확인
            user = Users.objects.get(username=user_id)
        except Users.DoesNotExist:
            pass
        else:
            # 비밀번호 확인
            try:
                # 앞의 argon2 제거 후 비교
                PasswordHasher().verify(user.password[6:], data.get('password'))
            except exceptions.VerifyMismatchError:
                pass
            else:
                # 성공
                login(request, user)

                res = ('로그인에 성공하였습니다.', 'success', 200)

        return res
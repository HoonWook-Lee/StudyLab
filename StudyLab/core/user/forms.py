from django import forms
from re import match as re_match
from argon2 import PasswordHasher, exceptions
from django.contrib.auth import login, logout
from random import randrange
import requests
from datetime import datetime, timedelta
from core.models import Users
from config.settings import DRF_DOMAIN



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
                try:
                    login(request, user)

                    now = datetime.now() # 현재
                    end_session = (      # 1주 만료 or 첫 로그인
                        lambda create : now if create is None else create + timedelta(weeks=1)
                    )(user.token_created_at)
                    
                    # DB 저장 토큰이 없거나 만료 시 토큰 생성
                    if user.token is None or now >= end_session:
                        token = requests.post(
                            f'{DRF_DOMAIN}/api/token/',
                            json = {'username' : user_id, 'password' : data.get('password')}
                        ).json()

                        user.token = token['refresh']
                        user.token_created_at = now
                        user.save()

                    res = ('로그인에 성공하였습니다.', 'success', 200)
                except:
                    res = ('잠시 후 다시 시도하여 주세요!', 'error', 500)

        return res

# 초기화 Form
class ResetForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'user_id', 'class' : 'form-control', 'placeholder' : '아이디를 입력해주세요', 'autofocus' : 'autofocus'
    }))

    hint = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'hint', 'class' : 'form-control', 'placeholder' : '가장 기억에 남는 한마디를 남겨주세요 (꼭 기억해주세요)'
    }))

    # 초기화
    def reset(self, data):
        # 무작위 4자리 숫자
        random_number = randrange(1000, 10000)

        res = ('정보가 일치하지 않습니다.', 'error', 422)

        try:
            # 등록 정보 확인
            user = Users.objects.get(username=data.get('user_id'))
        except Users.DoesNotExist:
            pass
        else:
            # 비밀번호 힌트 일치 시 비밀번호 초기화
            if user.hint == data.get('hint'):
                user.password = 'argon2' + PasswordHasher().hash(str(random_number))
                user.save()

                res = (f'변경된 비밀번호는 {random_number}입니다. \n 로그인 후 비밀번호를 변경하여 주세요.', 'success', 200)

        return res
    
# 비밀번호 변경 Form
class ChangeForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'user_id', 'class' : 'form-control', 'placeholder' : '아이디를 입력해주세요', 'autofocus' : 'autofocus'
    }))

    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'id' : 'password', 'class' : 'form-control', 'placeholder' : '비밀번호를 입력해주세요',
        'aria-describedby' : 'password', 'autocomplete' : 'off'
    }))

    check_password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'id' : 'check_password', 'class' : 'form-control', 'placeholder' : '비밀번호를 한번 더 입력해주세요',
        'aria-describedby' : 'password', 'autocomplete' : 'off'
    }))

    # 비밀번호 변경
    def change(self, request, data):
        # 6자 이상, 최소 하나의 문자, 숫자, 특수 문자를 포함한 문자
        pw = data.get('password')
        result = re_match('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{6,}$', pw)

        # 가능 유무 확인
        if result is None:
            res = ('비밀번호는 반드시 하나 이상의 \n 영문자, 숫자, 특수 문자를 포함한 \n 6자리 이상 조합이여야 합니다.', 'error', 422)
        elif pw != data.get('check_password'):
            res = ('비밀번호가 일치하지 않습니다.', 'error', 422)
        else:
            # 비밀번호 변경
            user = Users.objects.get(pk=request.user.id)
            user.password = 'argon2' + PasswordHasher().hash(pw)
            user.save()

            # 로그 아웃 시 모든 세션 제거
            request.session.clear()
            logout(request)
            
            res = ('비밀번호 변경이 완료되었습니다.', 'success',  200)

        return res
    
# 비밀번호 변경 Form
class WithdrawalForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.HiddenInput(attrs={
        'id' : 'user_id', 'class' : 'form-control'
    }))

    def delete(self, data):
        # 유저 확인
        user = Users.objects.get(pk=data.get('user_id'))

        user.delete()

        res = ('탈퇴가 완료되었습니다.', 'success',  200)

        return res
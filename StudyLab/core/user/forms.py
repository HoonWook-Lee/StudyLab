from django import forms


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


# 로그인 Form
class LoginForm(forms.Form):
    user_id = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'user_id', 'class' : 'form-control', 'placeholder' : '아이디를 입력해주세요', 'autofocus' : 'autofocus'
    }))

    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(attrs={
        'id' : 'password', 'class' : 'form-control', 'placeholder' : '비밀번호를 입력해주세요',
        'aria-describedby' : 'password', 'autocomplete' : 'off'
    }))
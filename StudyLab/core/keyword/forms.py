from django import forms


# 키워드 Form
class KeywordForm(forms.Form):
    # 키워드, 최대 100자, 필수값, input 위젯 지정
    keyword = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'keyword', 'class' : 'form-control', 'placeholder' : '키워드를 입력하여 주세요 (100자 이내)',
        'autofocus' : 'autofocus', 'style': 'font-size : 20px'
    }))
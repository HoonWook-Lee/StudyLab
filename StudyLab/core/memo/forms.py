from django import forms


# 메모 Form
class MemoForm(forms.Form):
    # 제목, 최대 100자, 필수값, input 위젯 지정
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'id' : 'title', 'class' : 'form-control', 'placeholder' : '제목을 입력하여 주세요',
        'autofocus' : 'autofocus', 'minlength' : 5, 'style' : 'font-size : 20px'
    }))

    # 본문, 필수값, Textarea 위젯 지정
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={
        'id' : 'content', 'class' : 'form-control', 'placeholder' : '메모 내용을 작성하여 주세요',
        'aria-label' : 'With textarea', 'rows' : '15'
    }))

    # 이미지, input 파일 위젯 지정
    img = forms.FileField(widget=forms.FileInput(attrs={
        'id' : 'img', 'class' : 'form-control', 'type' : 'file'
    }))
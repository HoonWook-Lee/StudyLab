from django.shortcuts import render


# 메인화면
def index(request):

    return render(request, 'main.html')
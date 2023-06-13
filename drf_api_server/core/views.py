from django.shortcuts import redirect


# 메인 화면 페이지 => /api/docs로 이동
def index(request):

    return redirect('/apis')
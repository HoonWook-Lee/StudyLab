from django.shortcuts import redirect
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController


api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController) # Token


# 메인 화면 페이지 => /api/docs로 이동
def index(request):

    return redirect('/api/docs')
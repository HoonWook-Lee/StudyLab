from django.shortcuts import redirect
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from core.search.apis import router as search_router


api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController) # Token
api.add_router('/search', search_router) # 검색 관련 API 모음


# 메인 화면 페이지 => /api/docs로 이동
def index(request):

    return redirect('/api/docs')
from django.shortcuts import redirect
from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja.errors import ValidationError
from django.http.response import JsonResponse
from core.search.apis import router as search_router
from core.comment.apis import router as comment_router


api = NinjaExtraAPI()

api.register_controllers(NinjaJWTDefaultController) # Token

api.add_router('/search', search_router) # 검색 관련 API 모음
api.add_router('/comment', comment_router) # 댓글 관련 API 모음

# 오류 재정의
@api.exception_handler(ValidationError)
def validation_errors(request, exc):
    return JsonResponse(dict(msg='유효하지 않은 정보입니다.'), status=422)


# 메인 화면 페이지 => /api/docs로 이동
def index(request):
    return redirect('/api/docs')
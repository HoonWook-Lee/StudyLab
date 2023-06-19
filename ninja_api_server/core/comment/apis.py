from ninja import Router
from ninja_jwt.authentication import JWTAuth
from django.http.response import JsonResponse
from core.comment.func import *


router = Router()


@router.get('/write', tags=['댓글 API 모음'], summary='메모 댓글 생성 API', auth=JWTAuth())
def comment_write(request, memo : int, writer : str, comment : str):
    """
    # 쿼리 파라미터 정보
    ## &emsp; memo : 메모 ID 정보, writer : username 정보, comment : 작성한 댓글 정보
    """
    # 객체 생성
    serializer = CommentFunc(memo)
    # 댓글 생성
    serializer.create(writer, comment)

    return JsonResponse(serializer.json, status=serializer.status_code, safe=False)
from re import match as re_match
from core.models import Users


# 아이디 중복 확인
def user_check_func(user_id):

    res = ('현재 등록된 아이디입니다.', 'error', 422)

    try:
        # 등록 정보 확인
        Users.objects.get(username=user_id)
    except:
        # 영소문자로 시작하는 5~20자 영문 소문자, 숫자와 특수기호(_),(-) 사용 문자
        result = re_match('^[a-z][a-z\d_-]{4,19}$', user_id)

        # 포함하지 않는 ID 제외
        res = (
            lambda id : (('영소문자로 시작하는 5 ~ 20자리의 \n 영소문자, 숫자, 특수기호(_),(-) \n 조합만 사용 가능합니다.', 'error', 422))
                if id is None else (('가입 가능한 아이디입니다.', 'success', 200))
        )(result)

        return res

    return res
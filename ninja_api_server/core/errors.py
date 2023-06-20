# 등록 정보 오류
class NotRegister(Exception):
    def __init__(self):
        super().__init__('등록되지 않은 사용자 및 메모 정보입니다.')

# 응답 오류
class NotResponse(Exception):
    def __init__(self):
        super().__init__('잠시 후 다시 이용해 주세요.')

# 댓글 오류
class NotComment(Exception):
    def __init__(self):
        super().__init__('존재하지 않는 댓글 정보입니다.')

# 접근 권한 오류
class NotAccess(Exception):
    def __init__(self):
        super().__init__('수정 및 삭제 권한을 가지고 있지 않습니다.')
# 등록 정보 오류
class NotRegister(Exception):
    def __init__(self):
        super().__init__('등록되지 않은 사용자 및 메모 정보입니다.')

# 응답 오류
class NotResponse(Exception):
    def __init__(self):
        super().__init__('잠시 후 다시 이용해 주세요.')
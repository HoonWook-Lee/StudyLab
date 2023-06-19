from datetime import datetime
from core.models import Memos, Users
from core.dynamodb import Comments
from core.errors import *

# 현재 시간 데코레이터 생성
def time_logger(func):
    def wrapper(self, *args):
        # 현재 시간 변경
        self.created_at = f'{datetime.now()}'
        # 함수 실행
        func(self, *args)

    return wrapper

# 댓글 관련 함수 킄래스
class CommentFunc:

    # 생성자 : 메모 ID, 생성 시간, 응답 Json, 상태 코드
    def __init__(self, memo):
        self.memo = memo
        self.created_at = None
        self.json = dict()
        self.status_code = 200

    @time_logger
    def create(self, writer, comment):

        try:
            # 등록된 메모 및 사용자 체크
            memo = Memos.objects.filter(id=self.memo)
            user = Users.objects.filter(username=writer)

            # 등록되지 않은 메모 오류 처리
            if not memo or not user:
                self.status_code = 404
                raise NotRegister

            check = 0 # 반복 횟수 측정

            while True:

                # 등록 정보 확인
                resp = Comments.get_item(Key={ 'Memo' : self.memo, 'Created_at' : self.created_at})

                if 'Item' not in resp:
                    # 댓글 등록
                    item = dict(
                        Memo = self.memo, Created_at = self.created_at,
                        Comment = dict(Comment=comment, Writer = writer, Updated_at = self.created_at)
                    )
                    Comments.put_item(Item=item)

                    break # 등록 시 반복 해제
                else:
                    # 중복 시 시간 변화
                    self.created_at = f'{datetime.now()}'

                    # 무한 루프 오류 처리
                    check += 1
                    if check > 10:
                        raise NotResponse

        except (NotRegister, NotResponse) as e:   # 확인된 에러 메세지
            self.json['msg'] = f'{e}'
            self.status_code = 422

        except Exception as e:   # 알 수 없는 에러 메세지
            self.json['msg'] = f'알 수 없는 오류 발생 잠시 후 다시 이용해주세요.'
            self.status_code = 500

        else:
            self.json['msg'] = '댓글 등록이 완료되었습니다.'
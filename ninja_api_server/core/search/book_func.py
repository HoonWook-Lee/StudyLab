import requests
from config.settings import env

# res error class 생성
class ResErrorClass:
    # 생성자
    def __init__(self):
        self.status_code = 500

    # 에러 메세지 전송
    @staticmethod
    def json():
        send = dict(errorMessage='잠시 후 다시 시도하여 주세요!')

        return send

# 책 목록 가져오기
async def search_book_func(keyword, page):

    # 페이지 당 9개 view
    start = (9 * page) - 8
    
    try:
        res = requests.get(
            f'{env("NAVER_API_BOOK")}?query={keyword}&display=9&start={start}', 
            headers = {
                'X-Naver-Client-Id' : env('NAVER_API_ID'),
                'X-Naver-Client-Secret' : env('NAVER_API_SECRET')
            }
        )
    except:
        res = ResErrorClass()

    return res

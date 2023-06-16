from requests import get
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from config.settings import env
from core.models import Crawling, Crawling_message

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
        res = get(
            f'{env("NAVER_API_BOOK")}?query={keyword}&display=9&start={start}', 
            headers = {
                'X-Naver-Client-Id' : env('NAVER_API_ID'),
                'X-Naver-Client-Secret' : env('NAVER_API_SECRET')
            }
        )
    except:
        res = ResErrorClass()

    return res

# 데이터 최신화 확인
async def crawling_check_func():
    # 1주일 전
    weeks = datetime.now() - timedelta(weeks=1)

    # 데이터가 없거나 1주일 주기로 최신화 check
    if Crawling.check_data() == 0:
        return True
    else:
        return (
            lambda create, week : True if create < week else False
        )(Crawling_message.objects.latest('updated_at').updated_at, weeks)

# 데이터 수집 메시지 저장
async def crawling_message_func(send):
    if send :
        now = datetime.now().strftime('%Y년 %m월 %d일')
        instance = Crawling_message()
        instance.message = f'{now} 데이터 최신화 완료'

        instance.save()
    else:
        instance = Crawling_message()
        instance.message = '데이터 수집 중 입니다.'

        instance.save()

    return instance

# 마지막 페이지 정보 가져오기
async def crawling_end_func(base_url):
    
    response = get(base_url)

    if response.status_code == 200:
        try:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            end_page = soup.find_all('a', 'link_num')[-1].find('span', '').text
        except:
            end_page = 0
    else:
        end_page = 0
    
    return end_page

# 책 크롤링 정보 가져오기
async def crawling_book_func(session, url, i):

    res = list()

    async with session.get(url) as response:
        # html 수집
        html = await response.text() 
        soup = BeautifulSoup(html, 'html.parser')

        # 모든 li 수집
        list_article = soup.find_all('li', '')

        for txt in list_article:
            # txt_thumb인 첫 번째 p 태그 수집
            title = txt.find('p', 'txt_thumb')
            # txt_thumb인 모든 p 태그 수집
            content = txt.find_all('p', 'txt_thumb')
            # date인 첫 번째 span 태그 수집
            date = txt.find('span', 'date')
            # a 링크의 href 값 수집
            link = txt.find('a', 'link_thumb')

            # None을 제외한 나머지 내용 수집
            if title is not None and content is not None and date is not None:
                res.append(dict(title=title.text, content=content[-1].text, date=date.text, link=link.attrs['href']))
            
    return res
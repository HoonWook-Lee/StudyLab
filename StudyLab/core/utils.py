import requests
from datetime import datetime, timedelta
from config.settings import DRF_DOMAIN

def check_token(request):

    # 현재 시간
    now = datetime.now()

    # Token 가져오기
    try:
        if f'{request.user}' not in request.session.keys() or \
            request.session.get(f'{request.user}_time') < f'{now - timedelta(minutes=30)}':
                
                token = requests.post(
                    f'{DRF_DOMAIN}/api/token/refresh/',
                    json = {'refresh' : request.user.token}
                ).json()['access']
                
                # 만료 시간 확인 위한 값 추가
                request.session[f'{request.user}'] = token
                request.session[f'{request.user}_time'] = f'{now}'
        else:
            token = request.session[f'{request.user}']
    except:
        token = None
    
    return token
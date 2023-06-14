from apscheduler.schedulers.background import BackgroundScheduler
from core.scheduler.func import check_memo
from config.settings import TIME_ZONE
 

# 스케줄러 작업
def cron_jobs():

    scheduler = BackgroundScheduler(timezone=TIME_ZONE)

    # 1분 마다 욕설이 들어간 메모 삭제
    # interval : 시간 간격, cron : 매 시간, 매 초, 매 분 마다 실행
    scheduler.add_job(check_memo, 'interval', minutes = 1) 

    scheduler.start()
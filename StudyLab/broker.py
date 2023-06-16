import os
import django
from pika import URLParameters, BlockingConnection
from json import loads
from config.settings import env

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# URL 파라미터 : cloudamqp에서 URL 생성
params = URLParameters(env('Rabbit_URL'))

# 연결
connection = BlockingConnection(params)

# 통로 연결
channel = connection.channel()

# 큐 선언
channel.queue_declare(queue='StudyLab')

# 메세지 시 행동 함수
def callback(ch, method, properties, body):
    print('Received API')
    data = loads(body)

    from core.models import Crawling

    if properties.content_type == '데이터 최신화 완료':
        for item in data['items']:
            for i in item:
                try:
                    Crawling.objects.get(title=i['title'])
                except:
                    instance = Crawling()
                    instance.title = i['title']
                    instance.content = i['content']
                    instance.date = i['date']
                    instance.link = i['link']
                    instance.save()

channel.basic_consume(queue='StudyLab', on_message_callback=callback, auto_ack=True)

print('Start')

channel.start_consuming()

channel.close() 
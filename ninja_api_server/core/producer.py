import pika
import json
from config.settings import env

# URL 파라미터 : cloudamqp에서 URL 생성
params = pika.URLParameters(env('Rabbit_URL'))

# 연결
connection = pika.BlockingConnection(params)

# 통로 연결
channel = connection.channel()

# 메세지 전달 함수
def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='StudyLab', body=json.dumps(body), properties=properties)
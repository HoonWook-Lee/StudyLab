#!/bin/bash

# 실패 시 script 실행 중지
set -e

# static 파일 모음 있다면 -yes 명령어 실행
echo yes | python3 manage.py collectstatic

# DB Migrate
python3 manage.py makemigrations 
python3 manage.py migrate

# Uvicorn 실행
uvicorn config.asgi:application --host=0.0.0.0 --port=5000
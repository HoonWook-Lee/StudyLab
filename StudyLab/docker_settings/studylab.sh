#!/bin/bash

# 실패 시 script 실행 중지
set -e

# static 파일 모음 있다면 -yes 명령어 실행
echo yes | python3 manage.py collectstatic

# DB Migrate
python3 manage.py makemigrations 
python3 manage.py migrate

# 실행 폴더 생성
mkdir run

# gunicorn 실행
gunicorn --bind unix:/var/www/studylab/run/gunicorn.sock config.wsgi:application
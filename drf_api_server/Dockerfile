FROM python:3.11.3

# 보조 설명
LABEL maintainer="gnsdnr1022@gmail.com"
LABEL description="Django Rest API 배포"

# Update
RUN apt-get update

# 유저를 추가, 패스워드 입력하지 않고 홈 디렉토리를 생성
RUN adduser --disabled-password python

# 유저 변경 (root -> python)
USER python

# 프로젝트 디렉토리 복사 (python 유저에게 권한 부여)
COPY --chown=python:python ./ /var/www/drf_api_server

# 프로젝트 디렉토리로 이동
WORKDIR /var/www/drf_api_server

# 해당 유저로 의존성 패키지 설치
RUN pip install --user -r requirements.txt

# 설치한 패키지 명령어 사용을 위해 환경변수등록
ENV PATH="/home/python/.local/bin:${PATH}"

# 포트 5000 개방
EXPOSE 5000

# 엔트리포인트 실행권한 추가
RUN chmod +x ./docker_settings/studylab.sh 

# gunicorn 실행
# CMD sh ./docker_settings/studylab.sh 
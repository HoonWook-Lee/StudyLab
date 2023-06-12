# StudyLab

> StudyLab은 자신이 가진 기술을 소개하고 필요한 내용을 얻을 수 있는 개발 관련 커뮤니티입니다.   
> 프로젝트 관련 자세한 정보는 [Wiki](https://github.com/HoonWook-Lee/StudyLab/wiki)에서 확인할 수 있습니다.

## 1. 사용한 Framework

> [Django](https://docs.djangoproject.com) : 파이썬으로 만들어진 무료 오픈소스 웹 애플리케이션 프레임워크   
> [Django REST Framework](https://www.django-rest-framework.org/) : Django REST 프레임워크는 웹 API 구축을 위한 강력하고 유연한 툴킷   
> [Django Ninja](https://django-ninja.rest-framework.com/) : Django 및 Python 3.6+ 유형 힌트로 API를 구축하기 위한 웹 프레임워크


## 2. Coding Convention

> 여러사람이 협업을 해도 모두가 읽기 편한 코드를 작성하기 위한 기본 규칙   
> But Local Rule이 더 중요!!

```
* 한 줄의 문자열은 79자, Django는 119자 추천
* DocString은 72자
* snake_case 사용
* 모듈 레벨 상수는 모두 대문자
* ClassName은 Capitalized Word
* 한 줄로 된, if, try...except, for, while 구문은 사용하지 않는다.
```

## 3. 개발 환경 설정

```sh
* 개발 운영 체제 : macOS
* 배포 운영 체제 : EC2 ( Ubuntu 20.04 )
* 사용한 DB : MySQL 8.0
* Python Version : Python 3.11.3
* Frontend : Django-Template + Vue.js
* Backend Framework : Django
* API Framework : Django Ninja + Django REST Framework
* Web Server : Nginx
* Web Server Gateway Interface : Gunicorn
* ASGI : Uvicorn
```
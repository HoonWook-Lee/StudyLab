from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser 사용
class Users(AbstractUser):
    # 문자열 최대 50자
    hint = models.CharField(max_length=50)
    token = models.CharField(max_length=400, blank=True, null=True) # Token
    token_created_at = models.DateTimeField(null=True) # Token 저장 시간

# 작성, 수정 시간을 상속
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) # Date 처음 생성 시 설정
    updated_at = models.DateTimeField(auto_now=True) # Date 저장 시 설정

    # 선언함으로써, 다른 모델들이 상속 받을 수 있는 모델이 된다.
    class Meta:
        abstract = True

DEFAULT_ADMIN_PK = 1 # 관리자 PK값

# 키워드 모델 생성
class Keywords(TimeStampedModel):
    # 문자열 최대 100자
    keyword = models.CharField(max_length=100)
    # 유저 삭제 시 관리자로 변경
    writer = models.ForeignKey(Users, on_delete=models.SET_DEFAULT, default=DEFAULT_ADMIN_PK)

# 메모 모델 생성
class Memos(TimeStampedModel):
    title = models.CharField(max_length=100) # 문자열 최대 100자
    content = models.TextField() # 큰 텍스트 필드 
    # 유저 삭제 시 관리자로 변경
    writer = models.ForeignKey(Users, on_delete=models.SET_DEFAULT, default=DEFAULT_ADMIN_PK) 
    like = models.BigIntegerField(default=0) # 64비트 정수 기본값 = 0
    # blank = 폼에서 비워둘 수 있음, null = Null 저장 허용
    img = models.FileField(upload_to='', blank=True, null=True) 
    # 다대다 관계, Null 허용, 폼 비움 허용
    keywords = models.ManyToManyField('Keywords', related_name='memos', blank=True)
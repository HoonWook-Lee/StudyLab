from django.db import models
from django.contrib.auth.models import AbstractUser


# AbstractUser 사용
class Users(AbstractUser):
    # 문자열 최대 50자
    hint = models.CharField(max_length=50)
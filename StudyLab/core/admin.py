from django.contrib import admin
from core.models import *


# 페이지 관리 DB
admin.site.register(Users)
admin.site.register(Memos)
admin.site.register(Keywords)
from django.apps import AppConfig
from os import environ
from core.scheduler import cron


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):

        # 2번 실행 방지
        if environ.get('RUN_MAIN', None) != 'true':
            cron.cron_jobs()

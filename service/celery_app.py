import os
import time

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")

app = Celery('service')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(20)
    print('Request: {0! Hello Debug Task!}')

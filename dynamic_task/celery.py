import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynamic_task.settings')

app = Celery('dynamic_task')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
# app.conf.beat_max_loop_interval = 10


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

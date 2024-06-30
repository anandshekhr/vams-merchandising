from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vams_merchandise.settings')

app = Celery('vams_merchandise')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

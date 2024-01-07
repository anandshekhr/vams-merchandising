from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vams_merchandise.settings')

app = Celery('vams_merchandise')
app.conf.enable_utc = False

app.conf.update(timezone = settings.CELERY_TIMEZONE)
app.config_from_object(settings,namespace='CELERY')

#celery beat settings
app.conf.beat_schedule = {

}


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
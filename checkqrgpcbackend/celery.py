from __future__ import absolute_import
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      'checkqrgpcbackend.settings.development')
app = Celery('checkqrgpcbackend')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()


@app.task
def test_task():
    return 'Here testing task'
import os

from celery import Celery
from pytz import timezone
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Elearning.settings')

app = Celery('Elearning')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'my_task': {
#         'task': 'subject.task.sendemail',
#         'schedule':crontab(hour=10, minute=47),
#         #'args':
#     },
# }
app.conf.update(timezone = 'Asia/Kolkata')


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
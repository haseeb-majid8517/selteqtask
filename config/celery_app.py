import os

from celery import Celery
# from celery.task import periodic_task
from datetime import timedelta
import logging
# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("selteq_task")
logger = logging.getLogger(__name__)
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'user-tasks': {
        'task': 'selteq_task.users.tasks.user_tasks',  # Specify the task path
        'schedule': timedelta(minutes=1),    # Set the schedule interval
    },
}

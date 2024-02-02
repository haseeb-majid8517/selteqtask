from django.contrib.auth import get_user_model
from .models import *
from config import celery_app
import logging
User = get_user_model()
logger = logging.getLogger(__name__)


@celery_app.task()
def user_tasks():
    # Add your task logic here
    tasks = Task.objects.all()
    for task in tasks:
        task_info = f'Task Name: {task.task_name}, Created At: {task.created_at}'
        print(task_info)



from datetime import datetime
import time
from huey.contrib.djhuey import periodic_task, task
from huey import crontab
#from .huey import huey
#from time import sleep
#from django_huey import huey
#from .views import get_live_stream
from myapp.services import get_live_stream
from django.utils import timezone
from .models import MyModel


# Переменная для контроля начала задач
task_started = False


@task
def periodic_task(task_id):
    task = MyModel.objects.get(id=task_id)
    task.last_run = timezone.now()
    task.save()
    print(f"Task '{task.name}' выполнена в {task.last_run}")


"""
@task
def my_periodic_task(channel_id):
    # Логика выполнения задачи
    current_timestamp = time.time()
    message = get_live_stream(channel_id, None)
    print("Task activated", message, f"Текущее время (в формате UNIX timestamp): {current_timestamp}")

@periodic_task  # Каждые 10 секунд
def periodic_task_function():
    global task_started
    while task_started:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Задача выполнена в {current_time}")
        sleep(10)  # Задержка в 10 секунд между выполнениями
"""
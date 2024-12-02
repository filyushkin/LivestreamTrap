from huey.contrib.djhuey import task
from huey import crontab
#from .huey import huey
from time import sleep
from django_huey import huey
from .views import get_live_stream

"""
"""

@huey.periodic_task()
def my_periodic_task():
    # Логика выполнения задачи
    message = get_live_stream(channel_id, API_KEY)
    print("Task activated")
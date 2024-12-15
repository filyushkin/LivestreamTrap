from huey.contrib.djhuey import task
#from huey import crontab
#from .huey import huey
#from time import sleep
#from django_huey import huey
#from .views import get_live_stream
from myapp.services import get_live_stream


@task
def my_periodic_task(channel_id, ):
    # Логика выполнения задачи
    message = get_live_stream(channel_id, None)
    print("Task activated", message)

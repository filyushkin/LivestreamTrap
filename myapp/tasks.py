from huey.contrib.djhuey import task

from myapp.services import get_live_stream


@task
def my_periodic_task(channel_id, ):
    # Логика выполнения задачи
    message = get_live_stream(channel_id, None)
    print("Task activated", message)

from huey.contrib.djhuey import task

"""
#from huey import periodic_task, crontab
from datetime import timedelta
#from myapp.models import TaskModel  # модель ваших задач
from huey.contrib.django import database_only
from myproject.huey import huey  # Подключаем экземпляр Huey
@periodic_task(crontab(minute='0'))  # каждую минуту или каждый час (час можно указать через crontab)
def execute_task(task_id):
    task = TaskModel.objects.get(id=task_id)
    print(f"Executing task {task.id}: {task.name}")
    # Добавьте логику выполнения задачи
@huey.periodic_task(crontab(minute='*'))
def my_minutely_task():
    print("This task runs every minute.")
    
   
@huey.task()
def long_running_task():
    # Эмуляция долгой работы
    import time
    time.sleep(10)  # Например, задержка 10 секунд
    print("Task finished!")
"""

@task()
def count_beans() -> str:
    print('-- counted %s beans --!!!!!!!!!!!!!!!!!!!!!!!')
    return 'Success!'

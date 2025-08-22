import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LivestreamTrap.settings')

app = Celery('LivestreamTrap')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Периодические задачи
app.conf.beat_schedule = {
    'update-channels-every-2.5-min': {
        'task': 'tracker.tasks.update_channels_info',
        'schedule': 150.0,  # 2.5 минуты = 150 секунд
    },
    'check-active-streams-every-5-min': {
        'task': 'tracker.tasks.check_active_streams',
        'schedule': 300.0,  # 5 минут = 300 секунд
    },
}

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LivestreamTrap.settings')
django.setup()

from tracker.models import Channel
from django.db import connection

# Проверим все каналы в базе
channels = Channel.objects.all()
print(f"Каналов в базе: {channels.count()}")
for channel in channels:
    print(f" - {channel.handle}")

# Проверим ограничения базы данных
with connection.cursor() as cursor:
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tracker_channel'")
    table_sql = cursor.fetchone()
    print(f"\nSQL создания таблицы:\n{table_sql[0]}")

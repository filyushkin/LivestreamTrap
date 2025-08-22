from __future__ import annotations
import os
import shlex
import subprocess
from pathlib import Path
from datetime import datetime, timezone
import logging

from celery import shared_task
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from .models import Channel, Task, StreamRecord
from .youtube_api import get_channel_info, get_current_streams

logger = logging.getLogger(__name__)

# Директории для файлов
STREAMS_DIR = Path(settings.MEDIA_ROOT) / "streams"
RECORDINGS_DIR = Path(settings.MEDIA_ROOT) / "recordings"
STREAMS_DIR.mkdir(parents=True, exist_ok=True)
RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)


def _run(cmd: str) -> int:
    """Запустить внешнюю команду и вернуть код выхода."""
    return subprocess.call(shlex.split(cmd), timeout=3600)  # 1 hour timeout


def _probe_duration_seconds(mp3_path: Path) -> int:
    """Получить длительность аудио через ffprobe."""
    try:
        out = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", str(mp3_path)
        ], timeout=30).decode().strip()
        return int(float(out))
    except Exception:
        return 0


@shared_task
def update_channels_info():
    """Обновляет информацию о каналах каждые 2.5 минуты"""
    channels = Channel.objects.all()

    for channel in channels:
        try:
            channel_info = get_channel_info(channel.handle)

            if channel_info:
                channel.name = channel_info.get('name', channel.name)
                channel.country = channel_info.get('country', channel.country)
                channel.subscribers_count = channel_info.get('subscribers_count', 0)

                # Проверяем текущие стримы
                current_streams = get_current_streams(channel.handle)
                channel.current_streams_count = len(current_streams)

                channel.save()
                logger.info(f"Обновлена информация для канала {channel.handle}")

        except Exception as e:
            logger.error(f"Ошибка при обновлении канала {channel.handle}: {str(e)}")


@shared_task
def monitor_channels():
    """
    Проверяет активные задачи и запускает запись при начале стрима
    """
    try:
        tasks = Task.objects.select_related("channel").filter(is_active=True)
        for task in tasks:
            if task.is_recording:
                continue

            current_streams = get_current_streams(task.channel.handle)
            if current_streams:
                # Запускаем запись первого найденного стрима
                start_recording_for_channel.delay(task.id, current_streams[0])

    except Exception as e:
        logger.error(f"Ошибка в monitor_channels: {str(e)}")


@shared_task
def start_recording_for_channel(task_id: int, stream_url: str):
    """Запускает запись стрима и конвертацию в MP3"""
    try:
        task = Task.objects.select_related("channel").get(id=task_id)
        channel = task.channel

        with transaction.atomic():
            task.refresh_from_db()
            if task.is_recording:
                return
            task.is_recording = True
            task.save(update_fields=["is_recording"])

        # Создаем уникальное имя файла
        timestamp = now().strftime("%Y%m%d_%H%M%S")
        ts_filename = f"{channel.handle}_{timestamp}.ts"
        mp3_filename = f"{channel.handle}_{timestamp}.mp3"

        ts_path = STREAMS_DIR / ts_filename
        mp3_path = RECORDINGS_DIR / mp3_filename

        # Запись с помощью ytarchive
        yt_cmd = f'ytarchive --audio-only "{stream_url}" "{ts_path}"'
        result = _run(yt_cmd)

        if result != 0:
            raise Exception(f"ytarchive завершился с кодом {result}")

        # Конвертация в MP3
        ffmpeg_cmd = f'ffmpeg -i "{ts_path}" -codec:a libmp3lame -qscale:a 2 "{mp3_path}"'
        result = _run(ffmpeg_cmd)

        if result != 0:
            raise Exception(f"ffmpeg завершился с кодом {result}")

        # Создаем запись в базе данных
        duration = _probe_duration_seconds(mp3_path)

        StreamRecord.objects.create(
            channel=channel,
            task=task,
            title=f"Запись {channel.handle} - {timestamp}",
            stream_url=stream_url,
            started_at=now(),
            duration_sec=duration,
            ts_relpath=f"streams/{ts_filename}",
            mp3_relpath=f"recordings/{mp3_filename}",
        )

        # Обновляем счетчик записей
        task.record_count += 1
        task.is_recording = False
        task.save(update_fields=["record_count", "is_recording"])

        logger.info(f"Успешно записан стрим для {channel.handle}")

    except Exception as e:
        logger.error(f"Ошибка записи стрима: {str(e)}")
        # Сбрасываем флаг записи при ошибке
        try:
            task.is_recording = False
            task.save(update_fields=["is_recording"])
        except:
            pass

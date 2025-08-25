from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from django.conf import settings

from .models import Channel, Task, StreamRecord
from .youtube_service import get_channel_stats  # Измененный импорт


def main(request):
    channels = Channel.objects.all().order_by('-created_at')

    if request.method == 'POST':
        handle = request.POST.get('channel_handle', '').strip()

        # Нормализация handle
        if handle.startswith('@'):
            handle = handle[1:]
        handle = handle.lower()

        if 'check_channel' in request.POST:
            if not 3 <= len(handle) <= 30:
                messages.error(request, "Псевдоним должен быть от 3 до 30 символов")
                return redirect('main')

            # Проверяем, существует ли уже канал
            existing_channels = Channel.objects.filter(handle__iexact=handle)
            if existing_channels.exists():
                messages.warning(request, "Канал с указанным псевдонимом был занесён в базу данных ранее")
                return redirect('main')

            # Получаем данные через YouTube API
            channel_info = get_channel_stats(handle)
            if not channel_info:
                messages.error(request, "Канала с указанным псевдонимом не существует или недоступен")
                return redirect('main')

            # Создаем новый канал
            try:
                with transaction.atomic():
                    published_at = parse_datetime(channel_info['published_at'])

                    channel = Channel(
                        handle=handle,
                        name=channel_info['name'],
                        country=channel_info['country'],
                        subscribers_count=channel_info['subscribers_count'],
                        current_streams_count=channel_info['current_streams_count'],  # Сохраняем стримы
                        channel_created_date=published_at.date() if published_at else None,
                        youtube_channel_id=channel_info['channel_id'],  # Сохраняем YouTube ID
                        description=channel_info['description']
                    )
                    channel.full_clean()
                    channel.save()
                    messages.success(request,
                                     "Канал с указанным псевдонимом найден, информация о нём занесена в базу данных")
            except ValidationError as e:
                messages.warning(request, f"Ошибка валидации: {e}")
            except Exception as e:
                messages.error(request, f"Ошибка при создании канала: {e}")

            return redirect('main')

        elif 'delete_channel' in request.POST:
            channel_id = request.POST.get('channel_id')
            try:
                channel = Channel.objects.get(id=channel_id)
                channel_name = channel.handle
                channel.delete()
                messages.info(request, f"Канал @{channel_name} удален")
            except Channel.DoesNotExist:
                messages.error(request, "Канал не найден")
            return redirect('main')

        elif 'create_task' in request.POST:
            channel_id = request.POST.get('channel_id')
            try:
                channel = Channel.objects.get(id=channel_id)

                if not Task.objects.filter(channel=channel, is_active=True).exists():
                    Task.objects.create(channel=channel)
                    messages.success(request, f"Задача для @{channel.handle} создана")
                else:
                    messages.warning(request, f"Для @{channel.handle} уже есть активная задача")
            except Channel.DoesNotExist:
                messages.error(request, "Канал не найден")
            return redirect('main')

    return render(request, 'tracker/main.html', {
        'channels': channels,
        'current_page': 'main'
    })


def tasks(request):
    tasks = Task.objects.select_related('channel').filter(is_active=True).order_by('-created_at')
    return render(request, 'tracker/tasks.html', {
        'tasks': tasks,
        'current_page': 'tasks'
    })


def downloads(request):
    recordings = StreamRecord.objects.select_related('channel', 'task').all().order_by('-created_at')
    return render(request, 'tracker/downloads.html', {
        'recordings': recordings,
        'current_page': 'downloads'
    })


@require_POST
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
        task.is_active = False
        task.save()
        messages.info(request, f"Задача для @{task.channel.handle} удалена")
    except Task.DoesNotExist:
        messages.error(request, "Задача не найдена")
    return redirect('tasks')


@require_POST
def delete_recording(request, recording_id):
    try:
        recording = StreamRecord.objects.get(id=recording_id)

        # Удаляем файлы
        import os
        from django.conf import settings

        if recording.ts_relpath:
            ts_path = settings.MEDIA_ROOT / recording.ts_relpath
            if os.path.exists(ts_path):
                os.remove(ts_path)

        if recording.mp3_relpath:
            mp3_path = settings.MEDIA_ROOT / recording.mp3_relpath
            if os.path.exists(mp3_path):
                os.remove(mp3_path)

        recording.delete()
        messages.info(request, "Запись удалена")
    except StreamRecord.DoesNotExist:
        messages.error(request, "Запись не найдена")
    return redirect('downloads')


def debug_database(request):
    """Страница отладки - показывает что действительно в базе"""
    channels = Channel.objects.all()
    channel_list = list(channels.values('id', 'handle', 'name'))

    return JsonResponse({
        'channels_count': channels.count(),
        'channels': channel_list,
        'all_handles': list(channels.values_list('handle', flat=True))
    })

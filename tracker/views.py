from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .forms import HandleForm
from .models import Channel, Task, StreamRecord
from pathlib import Path
import os

# --- Вспомогательное: заглушка "проверки" существования канала ---
# На следующем шаге заменим на реальную проверку (YouTube Data API / ytarchive).
def _fake_fetch_channel_info(handle: str) -> dict | None:
    """
    Возвращает словарь с данными о канале, если 'нашли'.
    Здесь всегда 'находим' — для обвязки БД и UI.
    """
    return {
        "title": handle,  # временно ставим handle как title
        "url": f"https://www.youtube.com/@{handle}",
        "country": "",
        "published_at": None,
        "subscribers": None,
        "live_count": 0,
    }

def main_view(request):
    form = HandleForm(request.POST or None)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'reset':
            messages.info(request, 'Поле очищено.')
            return redirect('main')

        if action == 'check':
            if form.is_valid():
                handle = form.cleaned_data['handle']
                # Уже есть в БД?
                if Channel.objects.filter(handle=handle).exists():
                    messages.warning(request, 'Канал с указанным псевдонимом был занесён в базу данных ранее')
                    return redirect('main')

                info = _fake_fetch_channel_info(handle)
                if info is None:
                    messages.error(request, 'Канала с указанным псевдонимом не существует')
                    return redirect('main')

                Channel.objects.create(
                    title=info["title"],
                    handle=handle,
                    url=info["url"],
                    country=info["country"],
                    published_at=info["published_at"],
                    subscribers=info["subscribers"],
                    live_count=info["live_count"],
                    has_task=False,
                )
                messages.success(request, 'Канал с указанным псевдонимом найден, информация о нём занесена в базу данных')
                return redirect('main')
            else:
                messages.error(request, 'Проверьте формат псевдонима.')
                return redirect('main')

        if action == 'delete':
            handle = request.POST.get('handle', '').strip().lower()
            ch = get_object_or_404(Channel, handle=handle)
            ch.delete()
            messages.info(request, f'Канал @{handle} удалён.')
            return redirect('main')

        if action == 'schedule':
            handle = request.POST.get('handle', '').strip().lower()
            ch = get_object_or_404(Channel, handle=handle)
            if ch.has_task:
                messages.warning(request, f'Для @{handle} задача уже поставлена.')
                return redirect('main')
            with transaction.atomic():
                Task.objects.create(channel=ch)
                ch.has_task = True
                ch.save(update_fields=['has_task'])
            messages.success(request, f'Для @{handle} задача поставлена.')
            return redirect('main')

    channels = Channel.objects.order_by('-created_at')
    return render(request, 'tracker/main.html', {
        'current_page': 'main',
        'form': form,
        'channels': channels,
    })

def tasks_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'unschedule':
            task_id = request.POST.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            channel = task.channel
            with transaction.atomic():
                task.delete()
                channel.has_task = False
                channel.save(update_fields=['has_task'])
            messages.info(request, f'Задача для @{channel.handle} снята.')
            return redirect('tasks')

    tasks = Task.objects.select_related('channel').order_by('-created_at')
    # Нужен формат для шаблона
    view_tasks = []
    for t in tasks:
        view_tasks.append({
            'id': t.id,
            'channel_title': t.channel.title,
            'handle': t.channel.handle,
            'created_at': t.created_at,
            'is_recording': t.is_recording,
            'record_count': t.record_count,  # в дальнейшем будем синхронизировать с фактом
        })
    return render(request, 'tracker/tasks.html', {
        'current_page': 'tasks',
        'tasks': view_tasks,
    })

def downloads_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            record_id = request.POST.get('record_id')
            rec = get_object_or_404(StreamRecord, id=record_id)
            # Удаляем файлы, если они есть физически
            media_root = Path(settings.MEDIA_ROOT)
            for rel in [rec.ts_relpath, rec.mp3_relpath]:
                if rel:
                    f = media_root / rel
                    try:
                        if f.exists():
                            os.remove(f)
                    except Exception:
                        pass
            rec.delete()
            messages.info(request, 'Запись удалена.')
            return redirect('downloads')

    records = StreamRecord.objects.select_related('channel', 'task').order_by('-created_at')
    view_records = []
    for r in records:
        mp3_url = None
        if r.mp3_relpath:
            mp3_url = settings.MEDIA_URL + r.mp3_relpath
        view_records.append({
            'id': r.id,
            'channel_title': r.channel.title,
            'started_at': r.started_at,
            'title': r.title,
            'mp3_url': mp3_url,
            'duration_str': r.duration_str,
        })
    return render(request, 'tracker/downloads.html', {
        'current_page': 'downloads',
        'records': view_records,
    })

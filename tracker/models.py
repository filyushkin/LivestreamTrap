from django.db import models

# Create your models here.

from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Channel(TimeStampedModel):
    title = models.CharField(max_length=255, help_text="Имя канала на YouTube")
    handle = models.CharField(max_length=30, unique=True, help_text="Псевдоним (handle) без @")
    url = models.URLField(help_text="Ссылка на канал")
    country = models.CharField(max_length=64, blank=True)
    published_at = models.DateField(null=True, blank=True)
    subscribers = models.PositiveIntegerField(null=True, blank=True)
    live_count = models.PositiveIntegerField(default=0)
    has_task = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title} (@{self.handle})"

class Task(TimeStampedModel):
    # Одна активная задача на канал
    channel = models.OneToOneField(Channel, on_delete=models.CASCADE, related_name='task')
    is_recording = models.BooleanField(default=False)
    record_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Задача для @{self.channel.handle}"

class StreamRecord(TimeStampedModel):
    # Запись завершённого стрима
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='records')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='records')
    title = models.CharField(max_length=255)
    started_at = models.DateTimeField()
    duration_sec = models.PositiveIntegerField(default=0)

    # Сохраняем ОТНОСИТЕЛЬНЫЕ пути внутри MEDIA_ROOT
    ts_relpath = models.CharField(max_length=500, blank=True)
    mp3_relpath = models.CharField(max_length=500, blank=True)

    def __str__(self) -> str:
        return f"{self.title} (@{self.channel.handle})"

    @property
    def duration_str(self) -> str:
        s = int(self.duration_sec or 0)
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        if h:
            return f"{h:d}:{m:02d}:{s:02d}"
        return f"{m:d}:{s:02d}"

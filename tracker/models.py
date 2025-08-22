from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
import re


class Channel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    handle = models.CharField(max_length=30)  # Без unique=True
    country = models.CharField(max_length=50, blank=True, null=True)  # Добавили null=True
    channel_created_date = models.DateField(null=True, blank=True)
    subscribers_count = models.IntegerField(default=0)
    current_streams_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Валидация handle на уровне модели"""
        import re
        if not re.match(r'^[a-zA-Z0-9_]{3,30}$', self.handle):
            raise ValidationError('Псевдоним может содержать только буквы, цифры и подчеркивания (3-30 символов)')

        # Проверяем уникальность handle (регистронезависимо)
        existing = Channel.objects.filter(handle__iexact=self.handle)
        if self.pk:
            existing = existing.exclude(pk=self.pk)
        if existing.exists():
            raise ValidationError('Канал с таким псевдонимом уже существует')

    def save(self, *args, **kwargs):
        self.full_clean()  # Вызываем валидацию
        self.handle = self.handle.lower()  # Приводим к нижнему регистру
        super().save(*args, **kwargs)

    @property
    def has_active_task(self):
        return self.task_set.filter(is_active=True).exists()

    def __str__(self):
        return f"@{self.handle}"

    class Meta:
        indexes = [
            models.Index(fields=['handle']),
        ]


class Task(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_recording = models.BooleanField(default=False)
    record_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Задача для @{self.channel.handle}"


class StreamRecord(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    stream_url = models.URLField(default="")
    started_at = models.DateTimeField()
    duration_sec = models.IntegerField(default=0)
    ts_relpath = models.CharField(max_length=200, blank=True)
    mp3_relpath = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_mp3_url(self):
        return f"/media/{self.mp3_relpath}" if self.mp3_relpath else ""

    def __str__(self):
        return self.title

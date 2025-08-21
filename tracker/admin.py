from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Channel, Task, StreamRecord

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("title", "handle", "country", "subscribers", "live_count", "has_task", "created_at")
    search_fields = ("title", "handle")

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("channel", "is_recording", "record_count", "created_at")

@admin.register(StreamRecord)
class StreamRecordAdmin(admin.ModelAdmin):
    list_display = ("title", "channel", "started_at", "duration_sec", "created_at")
    search_fields = ("title", "channel__handle")

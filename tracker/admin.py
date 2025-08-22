from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Channel, Task, StreamRecord

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        'handle',
        'name',
        'country',
        'subscribers_count',
        'current_streams_count',
        'has_active_task',
        'created_at'
    ]
    list_filter = ['country', 'created_at']
    search_fields = ['handle', 'name']
    readonly_fields = ['created_at']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        'channel',
        'is_active',
        'is_recording',
        'record_count',
        'created_at'
    ]
    list_filter = ['is_active', 'is_recording', 'created_at']
    search_fields = ['channel__handle', 'channel__name']
    readonly_fields = ['created_at']

@admin.register(StreamRecord)
class StreamRecordAdmin(admin.ModelAdmin):
    list_display = [
        'channel',
        'title',
        'started_at',
        'duration_sec',
        'created_at'
    ]
    list_filter = ['started_at', 'created_at']
    search_fields = ['channel__handle', 'title']
    readonly_fields = ['created_at']

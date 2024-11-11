from django.contrib import admin

# Register your models here.
from .models import MyModel, TaskChannel, Stream

admin.site.register(MyModel)
admin.site.register(TaskChannel)
admin.site.register(Stream)
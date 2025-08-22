from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('tasks/', views.tasks, name='tasks'),
    path('downloads/', views.downloads, name='downloads'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('downloads/delete/<int:recording_id>/', views.delete_recording, name='delete_recording'),
    path('debug/', views.debug_database, name='debug_db'),
]

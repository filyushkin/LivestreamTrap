from django.urls import path, include
from .views import my_view
from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.my_view, name='main'),
    path('tasks/', views.tasks, name='tasks'),
    path('downloads/', views.downloads, name='downloads')
]

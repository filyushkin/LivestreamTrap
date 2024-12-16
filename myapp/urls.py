from django.shortcuts import redirect
from django.urls import path, include
from .views import main
from django.urls import path
from . import views

urlpatterns = [
    path('', lambda request: redirect('main/')),
    path('main/', views.main, name='main'),
    path('tasks/', views.tasks, name='tasks'),
    path('downloads/', views.downloads, name='downloads')
]

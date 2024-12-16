import requests
import subprocess
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from .services import get_live_stream
from .tasks import my_periodic_task

from .models import MyModel

# Create your views here.

from .forms import MyModelForm

API_KEY = 'AIzaSyAdH-dstx0tnYHBKLG2BjrCRqmAV46AHyg'

# Глобальная переменная для контроля начала выполнения задач
task_started = False


def main(request):
    #form = MyModelForm #
    channel_name = ''
    message = ''
    tasks = ''
    
    if request.method == 'POST':
        #print(request.POST.get('dropdown_field'))
        #form = MyModelForm(request.POST) #
        
        tasks = MyModel.objects.all()
        
        form = MyModelForm(request.POST)
        if form.is_valid():
            if 'button_1' in request.POST:
                # Обработка кнопки 1
                channel_handle = form.cleaned_data['text_string_1']
                #channel_name, message = check_channel_exists(channel_handle)
                message = check_youtube_channel_exists(channel_handle, API_KEY)
                #message = "Button_1 pressed"
                #channel_name, message = check_youtube_channel_exists(channel_handle, API_KEY)
            #form.save()
            #return redirect('success')  # Замените на нужный URL
            if 'button_2' in request.POST:
                channel_handle = form.cleaned_data['text_string_1']
                channel_id = get_channel_id(channel_handle, API_KEY)
                message = get_live_stream(channel_id, API_KEY)
                #
            if 'button_3' in request.POST:                
                #youtube_url = message  # Укажите URL текущего стрима
                #record_stream(youtube_url, quality='audio_only')
                #interval = int(form.cleaned_data['interval'])
                #global task_started
                #task_started = True  # Устанавливаем флаг на True, чтобы задачи начали выполняться
                #periodic_task_function.apply_async()  # Запускаем задачу вручную, если нужно               
                name = request.POST.get('name')
                interval = int(request.POST.get('interval'))  # Получаем значение интервала из формы или данных

                # Создаем новую запись
                my_model_instance = MyModel.objects.create(name=name, interval=interval)
                my_model_instance.save()
                
                #model_instance = form.save()  # Сохраняем экземпляр MyModel в базе данных
                # Запускаем задачу
                my_periodic_task(my_model_instance.id)
                
                return redirect('tasks')
                #return HttpResponse("Задача была запланирована!")
    else:
        form = MyModelForm()
    
    #return render(request, 'myapp/my_template.html', {'form': form})

    return render(request, 'myapp/my_template.html', {
        'form': form,
        'channel_name': channel_name,
        'message': message,
        'subtitle': "Создать задачу на запись всех стримов с YouTube.",
        'tasks': tasks,
    })


def start_task(request):
    global task_started
    task_started = True  # Устанавливаем флаг на True, чтобы задачи начали выполняться
    periodic_task_function.apply_async()  # Запускаем задачу вручную, если нужно

    return JsonResponse({"status": "Задача началась, она будет выполняться каждые 10 секунд."})



def tasks(request):
    return render(request, 'myapp/tasks_template.html')


def downloads(request):
    return render(request, 'myapp/downloads_template.html')


"""
def check_channel_exists(handle):
    url = f'https://www.googleapis.com/youtube/v3/channels?part=snippet&forUsername={handle}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if 'items' in data and len(data['items']) > 0:
        channel_title = data['items'][0]['snippet']['title']
        return channel_title, f'Канал "{channel_title}" найден.'
    else:
        return '', 'Такого канала не существует.'
"""
def check_youtube_channel_exists(handle, api_key):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'q': handle,
        'type': 'channel',
        'part': 'snippet',
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            channel_title = data['items'][0]['snippet']['title']  # Получаем имя канала
            channel_id = data['items'][0]['id']['channelId']
            return f"Канал с псевдонимом '{handle}' найден. \n Имя канала: '{channel_title}'. \n ID канала: '{channel_id}'."
    
    return f"Канала с псевдонимом '{handle}' не существует."


def get_channel_id(channel_name, api_key):
    # URL для поиска на YouTube
    url = "https://www.googleapis.com/youtube/v3/search"

    # Параметры запроса
    params = {
        'part': 'snippet',
        'q': channel_name,
        'type': 'channel',
        'key': api_key
    }

    # Отправляем запрос к YouTube Data API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            # Получаем ID канала
            channel_id = data['items'][0]['id']['channelId']
            return channel_id
        else:
            return "Канал не найден."
    else:
        return f"Ошибка при выполнении запроса: {response.status_code}"


def record_stream(youtube_url, quality='best'):
    # Команда для записи текущего стрима с помощью ytarchive
    command = [
        'ytarchive', 
        '-w',                # Ожидать начала стрима
        '-q', #quality,       # Качество видео (например, best, 1080p)
        youtube_url, 
        quality#'best'
    ]

    # Запуск команды через subprocess
    try:
        subprocess.run(command, check=True)
        print("Запись завершена.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при записи: {e}")
        print("Подробная информация об ошибке:", e.stderr)
    except FileNotFoundError:
        print("ytarchive не найден. Убедитесь, что он установлен и доступен в PATH.")

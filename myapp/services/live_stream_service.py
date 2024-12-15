import requests


def get_live_stream(channel_id, api_key):
    # URL для поиска трансляций на YouTube
    url = "https://www.googleapis.com/youtube/v3/search"

    # Параметры запроса
    params = {
        'part': 'snippet',
        'channelId': channel_id,
        'eventType': 'live',  # Ищем только текущие трансляции
        'type': 'video',  # Тип контента - видео
        'key': api_key
    }

    # Отправляем GET-запрос к YouTube Data API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Проверяем, есть ли трансляция в ответе
        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            # Формируем ссылку на трансляцию
            live_url = f"https://www.youtube.com/watch?v={video_id}"
            return live_url
        else:
            return "Нет текущих трансляций на данном канале."
    else:
        return f"Ошибка при выполнении запроса: {response.status_code}"

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
import logging
import re

logger = logging.getLogger(__name__)


def get_youtube_service():
    """Создает и возвращает сервис для работы с YouTube Data API v3"""
    try:
        return build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    except Exception as e:
        logger.error(f"Ошибка создания YouTube сервиса: {e}")
        return None


def get_channel_stats(handle):
    """
    Получает статистику канала по handle
    Returns: dict с данными канала или None при ошибке
    """
    if not hasattr(settings, 'YOUTUBE_API_KEY') or not settings.YOUTUBE_API_KEY:
        logger.error("YouTube API key not configured")
        return None

    service = get_youtube_service()
    if not service:
        return None

    try:
        # Ищем канал по handle
        search_response = service.search().list(
            q=f'@{handle}',
            type='channel',
            part='id,snippet',
            maxResults=1
        ).execute()

        if not search_response.get('items'):
            return None

        channel_id = search_response['items'][0]['id']['channelId']

        # Получаем детальную информацию о канале
        channel_response = service.channels().list(
            id=channel_id,
            part='snippet,statistics,contentDetails,brandingSettings'
        ).execute()

        if not channel_response.get('items'):
            return None

        channel_data = channel_response['items'][0]
        snippet = channel_data['snippet']
        statistics = channel_data['statistics']
        branding = channel_data.get('brandingSettings', {})

        # Получаем текущие активные трансляции
        live_streams_count = get_current_live_streams(service, channel_id)

        return {
            'name': snippet['title'],
            'description': snippet.get('description', ''),
            'country': snippet.get('country', 'Не указана'),
            'subscribers_count': int(statistics.get('subscriberCount', 0)),
            'video_count': int(statistics.get('videoCount', 0)),
            'view_count': int(statistics.get('viewCount', 0)),
            'current_streams_count': live_streams_count,  # Добавляем количество стримов
            'published_at': snippet['publishedAt'],
            'thumbnail': snippet['thumbnails']['default']['url'],
            'channel_id': channel_id
        }

    except HttpError as e:
        logger.error(f"YouTube API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error getting channel stats: {e}")
        return None


def get_current_live_streams(service, channel_id):
    """
    Получает количество текущих активных трансляций на канале
    """
    try:
        # Ищем активные трансляции
        search_response = service.search().list(
            channelId=channel_id,
            type='video',
            eventType='live',  # Только live-трансляции
            part='id',
            maxResults=50
        ).execute()

        return len(search_response.get('items', []))

    except HttpError as e:
        logger.error(f"Error getting live streams: {e}")
        return 0
    except Exception as e:
        logger.error(f"Error in get_current_live_streams: {e}")
        return 0

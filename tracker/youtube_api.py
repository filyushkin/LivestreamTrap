import requests
from bs4 import BeautifulSoup
import logging
import re
from datetime import datetime
from urllib.parse import quote, unquote
import time

logger = logging.getLogger(__name__)


def normalize_handle(handle):
    """Нормализует handle: убирает @, приводит к нижнему регистру"""
    handle = handle.strip().lower()
    if handle.startswith('@'):
        handle = handle[1:]
    return handle


def get_channel_info(handle):
    """
    Получает информацию о канале через парсинг YouTube
    Возвращает dict с данными или None при ошибке
    """
    try:
        normalized_handle = normalize_handle(handle)
        url = f"https://www.youtube.com/@{normalized_handle}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            logger.warning(f"Канал {normalized_handle} не найден (статус: {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлекаем название канала из title страницы
        title_tag = soup.find('title')
        channel_name = title_tag.text.replace(' - YouTube', '').strip() if title_tag else normalized_handle

        # Извлекаем количество подписчиков
        subscriber_pattern = r'(\d+[\d,]*)\s*подписчик'
        subscribers_text = soup.get_text()
        subscribers_match = re.search(subscriber_pattern, subscribers_text)

        subscribers_count = 0
        if subscribers_match:
            try:
                subscribers_count = int(subscribers_match.group(1).replace(',', '').replace(' ', ''))
            except ValueError:
                pass

        # Пытаемся найти страну (гарантируем строку, а не None)
        country = ''
        country_pattern = r'страна[:\s]*([^\n\r]+)'
        match = re.search(country_pattern, subscribers_text, re.IGNORECASE)
        if match:
            country = match.group(1).strip()

        return {
            'name': channel_name,
            'handle': normalized_handle,
            'subscribers_count': subscribers_count,
            'country': country,  # Гарантированно строка, даже если пустая
            'created_date': datetime.now().date()
        }

    except Exception as e:
        logger.error(f"Ошибка получения информации о канале {handle}: {e}")
        return None

    except Exception as e:
        logger.error(f"Ошибка получения информации о канале {handle}: {e}")
        return None


def get_current_streams(handle):
    """
    Проверяет текущие активные стримы на канале
    Возвращает список URL активных стримов
    """
    try:
        normalized_handle = normalize_handle(handle)
        url = f"https://www.youtube.com/@{normalized_handle}/streams"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return []

        # Простая проверка на наличие live-стримов по тексту
        if 'live now' in response.text.lower() or 'прямой эфир' in response.text.lower():
            return [f"https://www.youtube.com/@{normalized_handle}/live"]

        return []

    except Exception as e:
        logger.error(f"Ошибка проверки стримов канала {handle}: {e}")
        return []

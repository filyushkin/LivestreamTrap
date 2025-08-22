from __future__ import annotations
import requests
from urllib.parse import urlparse, parse_qs

DEFAULT_HEADERS = {
    # Немного «человеческих» заголовков, чтобы не получить странную выдачу
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.8",
}

YOUTUBE = "https://www.youtube.com"

def resolve_channel_exists_by_handle(handle: str, timeout: float = 10.0) -> tuple[bool, str | None]:
    """
    Лёгкая проверка существования канала по handle без API:
    - GET https://www.youtube.com/@{handle} (follow redirects)
    - Если конечный URL уводит на /results?search_query=%40..., или код 404/410 -> считаем НЕ существует
    - Если остаётся /@handle или /channel/UC... -> считаем существует; возвращаем канонический URL
    """
    url = f"{YOUTUBE}/@{handle}"
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, allow_redirects=True, timeout=timeout)
    except requests.RequestException:
        return False, None

    # Явный 404/410 — не существует
    if resp.status_code in (404, 410):
        return False, None

    final = resp.url  # конечный URL после редиректов
    parsed = urlparse(final)

    # Если нас унесло на поисковую выдачу — считам, что такого канала нет
    if parsed.path.startswith("/results") and "search_query" in parse_qs(parsed.query):
        return False, None

    # Считаем валидным либо /@..., либо /channel/UC...
    if parsed.path.startswith("/@") or parsed.path.startswith("/channel/"):
        return True, final

    # Во всех прочих случаях — считаем «не найден»
    return False, None


def check_channel_live(handle: str, timeout: float = 10.0) -> tuple[bool, str | None]:
    """
    Проверка лайва:
    - GET https://www.youtube.com/@{handle}/live
    - При активном эфире YouTube редиректит на /watch?v=...
    - Возвращаем (is_live, watch_url | None)
    """
    url = f"{YOUTUBE}/@{handle}/live"
    try:
        resp = requests.get(url, headers=DEFAULT_HEADERS, allow_redirects=True, timeout=timeout)
    except requests.RequestException:
        return False, None

    final = resp.url
    parsed = urlparse(final)
    # Активный эфир: нас унесло на /watch
    if parsed.path == "/watch" and "v" in parse_qs(parsed.query):
        return True, final
    return False, None

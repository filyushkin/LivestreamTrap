# tracker/recording.py
import subprocess
from pathlib import Path


def record_stream(channel_handle, output_path):
    """Записывает стрим с помощью ytarchive"""
    # Создаем директорию если не существует
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    cmd = f"ytarchive --audio-only https://www.youtube.com/@{channel_handle} {output_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Ошибка записи: {result.stderr}")

    return output_path


def convert_to_mp3(input_path, output_path):
    """Конвертирует .ts в .mp3 с помощью ffmpeg"""
    cmd = f"ffmpeg -i {input_path} -acodec libmp3lame -q:a 2 {output_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Ошибка конвертации: {result.stderr}")

    # Удаляем исходный .ts файл после конвертации
    Path(input_path).unlink(missing_ok=True)

    return output_path

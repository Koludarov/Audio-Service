import os
from typing import Dict
import uuid

from pydub import AudioSegment


def generate_token() -> str:
    """Генерирует уникальный индентификатор"""
    return str(uuid.uuid4())


def create_folders(app, user_id):
    """Создаёт папки для файлов пользователя, если их не существует"""
    os.makedirs(app.config['UPLOAD_FOLDER'] + f'/{user_id}/mp3', exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'] + f'/{user_id}/wav', exist_ok=True)


def collect_file_data(app, filename, user_id) -> Dict[str, str]:
    """Собирает данные о файле"""

    file_uuid = generate_token()
    wav_path = os.path.join(app.config['UPLOAD_FOLDER']+ f'/{user_id}/wav', filename)
    mp3_path = f"recordings/{user_id}/mp3/{filename[:-4]}_{file_uuid}.mp3"
    data = {
        'file_uuid': file_uuid,
        'wav_path': wav_path,
        'mp3_path': mp3_path
    }

    return data


def convert_wav_to_mp3(wav_path, mp3_path):
    """Конвертирует формат файла из wav в mp3"""
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

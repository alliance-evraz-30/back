import os
from datetime import datetime
from pathlib import Path
import zipfile
from telebot import TeleBot


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_unique_file_name(chat_id: int, original_file_name: str) -> str:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{chat_id}_{timestamp}_{original_file_name}"


def save_file(bot: TeleBot, file_id: str, unique_file_name: str) -> Path:
    file_info = bot.get_file(file_id)

    downloaded_file = bot.download_file(file_info.file_path)

    local_path = os.path.join(UPLOAD_DIR, unique_file_name)

    with open(local_path, 'wb') as file:
        file.write(downloaded_file)

    if zipfile.is_zipfile(local_path):
        with zipfile.ZipFile(local_path, 'r') as zip_ref:
            extract_path = os.path.join(UPLOAD_DIR, os.path.splitext(unique_file_name)[0])
            zip_ref.extractall(extract_path)
        return Path(extract_path)

    return Path(local_path)


def get_output_path(input_path: str, extension: str) -> str:
    base_name = os.path.splitext(input_path)[0]
    return f"{base_name}{extension}"

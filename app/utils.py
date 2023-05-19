import datetime
import subprocess
import uuid


def generate_token() -> str:
    return str(uuid.uuid4())


def convert_wav_to_mp3(wav_path, mp3_path):
    subprocess.run(["ffmpeg", "-i", wav_path, mp3_path])

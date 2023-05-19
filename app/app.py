import logging
import os
from logging import config

from flask import Flask, request, jsonify, send_file


from database import db_session
from models import User, AudioRecord
from utils import generate_token, convert_wav_to_mp3, create_folders, collect_file_data

app_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app_dir, 'recordings')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

config.fileConfig('etc/logging.conf', disable_existing_loggers=False)

# Получение объекта логгера
logger = logging.getLogger(__name__)


@app.route("/users", methods=["POST"])
def create_user():
    """Добавление пользователя"""
    name = request.json.get("name")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    token = generate_token()
    user = User(name=name, token=token)
    db_session.add(user)
    db_session.commit()
    logger.info(f'Пользователь {user.id} создан')

    return jsonify({"user_id": user.id, "token": token}), 201


@app.route("/records", methods=["POST"])
def upload_audio():
    """Добавление аудиофайла в формате wav"""
    user_id = request.form.get("user_id")
    token = request.form.get("token")
    audio_file = request.files.get("audio")

    if not user_id or not token or not audio_file:
        return jsonify({"error": "Invalid request parameters"}), 400

    user = db_session.query(User).filter_by(id=user_id, token=token).first()

    if not user:
        return jsonify({"error": "Invalid user credentials"}), 401

    filename = audio_file.filename
    if filename[-4:] != '.wav':
        return jsonify({"error": "Unsupported Media Type, only '.wav' files can be upload"}), 415

    file_data = collect_file_data(
        app=app,
        filename=filename,
        user_id=user_id
    )

    create_folders(app=app, user_id=user_id)

    audio_file.save(file_data['wav_path'])
    convert_wav_to_mp3(file_data['wav_path'], file_data['mp3_path'])

    audio_record = AudioRecord(
        file_uuid=file_data['file_uuid'],
        filename=filename,
        wav_path=file_data['wav_path'],
        mp3_path=file_data['mp3_path'],
        user_id=user_id
    )
    db_session.add(audio_record)
    db_session.commit()
    logger.info(f'Запись {audio_record.id} добавлена')

    return jsonify({"download_url": f"http://127.0.0.1:8000/record?id={audio_record.id}&user={user.id}"}), 201


@app.route("/record", methods=["GET"])
def download_audio():
    """Получение аудиофайла в формате mp3"""
    record_id = request.args.get("id")
    user_id = request.args.get("user")

    if not record_id or not user_id:
        return jsonify({"error": "Invalid request parameters"}), 400

    try:
        audio_record = db_session.query(AudioRecord).filter_by(id=record_id, user_id=user_id).first()
    except Exception as error:
        logger.error(f'Ошибка при получении записи: {str(error)[:40]}')
        return jsonify({"error": "Invalid input syntax"}), 400

    if not audio_record:
        return jsonify({"error": "Audio record not found"}), 404

    return send_file(audio_record.mp3_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

FROM python:3.9

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR ./app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
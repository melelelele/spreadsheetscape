FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir fastapi uvicorn edge-tts

COPY . .

RUN if [ ! -f config.ini ]; then cp config.example.ini config.ini; fi

ENV FLASK_APP=game.py
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
EXPOSE 8765

CMD ["sh", "-c", "python tts_server.py & python game.py"]
FROM python:3.8-slim-bullseye
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && \
    pip install -r requirements.txt
CMD ["python", "app.py"]








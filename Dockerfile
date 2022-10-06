FROM python:3.8-slim-bullseye
COPY . /app
WORKDIR /app
RUN python --version
RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt
CMD ["python", "app.py"]








FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

# RUN python -m pip install --upgrade pip
RUN mkdir /app

COPY ./requirements.txt ./requirements-dev.txt /app

WORKDIR /app

RUN python -m pip install --no-cache-dir -r requirements.txt

# pre download model
RUN apt-get update && apt-get install libgl1 -y
RUN apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6
RUN python -c "from ultralytics import YOLO; YOLO('yolov8s.yaml')"

COPY . /app

EXPOSE 8080
CMD ["python", "run.py"]

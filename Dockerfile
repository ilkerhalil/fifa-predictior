FROM python:3.10

WORKDIR /app
RUN mkdir -p models
COPY dataset/* dataset/
COPY src/train.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
FROM python:3.10.12

WORKDIR /app
COPY src/train.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
CMD ["python", "./train.py"]
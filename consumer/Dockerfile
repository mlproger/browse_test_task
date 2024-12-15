FROM python:3

WORKDIR /app

COPY requirements.txt ./
COPY .env ./
COPY consumer/consumer.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "consumer.py"]
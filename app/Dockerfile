FROM python:3

WORKDIR /app

COPY requirements.txt ./
COPY .env ./
COPY app/main.py ./

RUN pip install --no-cache-dir -r requirements.txt

COPY producer/ ./

CMD ["python", "main.py"]
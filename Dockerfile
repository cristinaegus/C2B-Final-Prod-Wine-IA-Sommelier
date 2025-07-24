
# Dockerfile para Wine IA Production
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PORT=5001

CMD ["python", "app_sommelier.py"]

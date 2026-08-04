FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD gunicorn django_to_do_list.wsgi:application --bind 0.0.0.0:$PORT
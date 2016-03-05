FROM python:3-alpine

RUN pip install gunicorn

WORKDIR /
COPY app.py app.py
CMD gunicorn --bind :8000 app:app
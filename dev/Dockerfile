FROM --platform=linux/arm64 python:3.10-slim

# RUN apk upgrade -q --no-cache && \
#     apk update

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --upgrade pip \
    pip install -r requirements.txt

COPY ./project /app

WORKDIR /app

CMD ["python" ,"manage.py", "runserver", "0.0.0.0:8000"]

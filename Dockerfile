FROM python:3.11-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

ENV PYTHONUNBUFFERED True

COPY ./requirements.txt ${APP_HOME}/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
WORKDIR $APP_HOME

CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", \
    "--bind", ":8080", \
    "--workers", "1", \
    "--threads", "8", \
    "--timeout", "0", \
    "--chdir", "/app/src", \
    "main:app" ]



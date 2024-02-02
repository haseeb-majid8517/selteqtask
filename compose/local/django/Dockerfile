FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql \
        postgresql-contrib \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#COPY ./compose/local/django/entrypoint /entrypoint
#RUN sed -i 's/\r$//g' /entrypoint
#RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

# Set the working directory
WORKDIR /app

# Expose the PostgreSQL default port
EXPOSE 5432

# Copy and set entrypoint script
#COPY ./compose/local/django/entrypoint /entrypoint
#RUN sed -i 's/\r$//g' /entrypoint
#RUN chmod +x /entrypoint
#ENTRYPOINT ["/entrypoint"]

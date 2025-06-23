FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

ARG DEV=false


RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

RUN if [ "$DEV" = "true" ]; then \
      apt-get update && apt-get install -y git curl vim && \
      pip install -r /tmp/requirements.dev.txt; \
    fi

RUN adduser --disabled-password django-user

COPY ./app /app
WORKDIR /app
RUN chmod +x /app/entrypoint.sh
RUN chown -R django-user /app

USER django-user

EXPOSE 8000
ENTRYPOINT ["/app/entrypoint.sh"]

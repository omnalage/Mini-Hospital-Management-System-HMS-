FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc --no-install-recommends && rm -rf /var/lib/apt/lists/*

# install python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# copy project
COPY . /app

# entrypoint.sh is located at /app/entrypoint.sh after COPY from build context
# ensure it is executable regardless of working directory
RUN chmod +x /app/entrypoint.sh || true

WORKDIR /app/hms_backend


# collect static & apply migrations in entrypoint
ENV PORT 8000

CMD ["./entrypoint.sh"]

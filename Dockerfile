FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=national_drug_obs.settings

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    zlib1g \
    ca-certificates \
    openssl \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8080

CMD python manage.py migrate --noinput 2>&1; gunicorn national_drug_obs.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120 --access-logfile - --error-logfile -

#!/bin/bash
set -e

echo "Waiting for PostgreSQL using psycopg2..."

TRIES=0
until python -c "import psycopg2; psycopg2.connect(dbname='${POSTGRES_DB}', user='${POSTGRES_USER}', password='${POSTGRES_PASSWORD}', host='db')" \
    && echo "PostgreSQL is ready."; do
    TRIES=$((TRIES+1))
    if [ "$TRIES" -ge 30 ]; then
        echo "PostgreSQL did not become ready in time."
        exit 1
    fi
    echo "PostgreSQL not ready (attempt $TRIES/30), retrying in 2s..."
    sleep 2
done

echo "Applying migrations..."
python manage.py migrate

echo "Loading fixtures..."
python manage.py loaddata menu/fixtures/menu_items.json || echo "Fixture already loaded or failed"

echo "Starting server..."
exec "$@"

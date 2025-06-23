#!/bin/bash
set -e

echo "Waiting for PostgreSQL using psycopg2..."

TRIES=0
until python -c "
import psycopg2, os
from urllib.parse import urlparse

url = urlparse(os.environ['DATABASE_URL'])

psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)" && echo "PostgreSQL is ready."; do
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

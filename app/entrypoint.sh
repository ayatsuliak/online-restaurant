#!/bin/bash
set -e

echo "Waiting for PostgreSQL using psycopg2..."
python << END
import time
import psycopg2
import os

max_retries = 10
retry_delay = 2

for attempt in range(max_retries):
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB", "restaurant"),
            user=os.environ.get("POSTGRES_USER", "restaurant_user"),
            password=os.environ.get("POSTGRES_PASSWORD", "password"),
            host="db",
            port=5432
        )
        conn.close()
        print("PostgreSQL is ready.")
        break
    except psycopg2.OperationalError:
        print(f"PostgreSQL not ready (attempt {attempt + 1}/{max_retries}), retrying in {retry_delay}s...")
        time.sleep(retry_delay)
else:
    print("PostgreSQL did not become ready in time.")
    exit(1)
END

echo "Applying migrations..."
python manage.py migrate

echo "Loading fixtures..."
python manage.py loaddata menu/fixtures/menu_items.json || echo "Fixture already loaded or failed"

echo "Starting server..."
exec "$@"

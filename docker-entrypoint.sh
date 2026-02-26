#!/bin/bash
set -e

export PATH="/app/.venv/bin:$PATH"

echo "Применяем миграции"
alembic upgrade head

echo " Заполняем базу тестовыми данными"
PGPASSWORD=$POSTGRES_PASSWORD psql -U $POSTGRES_USER -d $POSTGRES_DB -h db -f seed.sql

echo "Запускаем приложение"
exec "$@"

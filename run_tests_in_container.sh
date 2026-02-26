#!/bin/bash

echo "Запускаем тесты внутри контейнера"

docker exec -i orgs-app bash << 'EOF'
set -e
echo "Активируем виртуальное окружение"
source /app/.venv/bin/activate

echo "Запускаем тесты"
pytest tests/test_read_api2.py -v

echo "Тесты завершены"
EOF



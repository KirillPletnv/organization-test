# Справочник организаций с информацией о зданиях и видах деятельности.
git clone https://github.com/KirillPletnv/organization-test.git
cd orgs-project
cp env .env
docker-compose up -d --build

# Тесты проверяют все GET-эндпоинты на реальной БД с конкретными данными.
chmod +x run_tests_in_container.sh
./run_tests_in_container.sh

# Скрипт check_api.sh последовательно проверяет все эндпоинты и показывает JSON-ответы.
chmod +x check_api.sh
./check_api.sh

# После запуска доступна автоматическая документация:
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

# Все запросы требуют заголовок: X-API-Key: secret-api-key-12345 (внесен по дефолту)

FROM python:3.12-slim  

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Создаём пользователя
RUN useradd --create-home --shell /bin/bash test_user

WORKDIR /app

# Устанавливаем зависимости
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && poetry config virtualenvs.in-project true && poetry install --no-interaction --no-ansi --no-root 
# Копируем код
COPY . .

# Меняем владельца на test_user
RUN chown -R test_user:test_user /app

# Скрипт запуска
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Переключаемся на пользователя
USER test_user

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["uvicorn", "orgs_project.main:app", "--host", "0.0.0.0", "--port", "8000"]

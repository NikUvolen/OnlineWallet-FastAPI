# Online Wallet API

FastAPI-приложение для работы с кошельками. Проект хранит баланс в PostgreSQL, использует Alembic для миграций и поддерживает запуск через Docker.

## Возможности

- создание кошелька
- получение баланса кошелька
- пополнение кошелька
- списание средств с проверкой остатка
- миграции базы данных через Alembic
- автозапуск тестов при старте контейнера приложения
- отдельный `pgAdmin` для просмотра базы

## Стек

- Python 3.14
- FastAPI
- SQLAlchemy async
- asyncpg
- Alembic
- pytest
- pytest-asyncio
- Ruff
- Docker / Docker Compose

## Структура проекта

- `app/` - код приложения
- `app/main.py` - точка входа FastAPI
- `app/wallets/` - логика кошельков
- `alembic/` - миграции базы данных
- `tests/` - pytest-тесты
- `scripts/entrypoint.sh` - запуск тестов, миграций и API в Docker
- `scripts/ensure_test_db.py` - создание тестовой базы

## API

Базовый префикс: `/v1`

### Создать кошелек

`POST /v1/wallets/`

Ответ:
```json
{
  "id": "986d69af-a78a-4111-8b33-befe923ff502",
  "balance": "0.00"
}
```

### Получить баланс

`GET /v1/wallets/{wallet_id}`

### Изменить баланс

`POST /v1/wallets/{wallet_id}/operation`

Тело запроса:
```json
{
  "operation_type": "DEPOSIT",
  "amount": 100.04
}
```

`operation_type` может быть:

- `DEPOSIT`
- `WITHDRAWAL`

## Переменные окружения

Файл локальной конфигурации: `app/.env`

Пример:

```env
POSTGRES_USER=wallet_user
POSTGRES_PASSWORD=wallet_password
POSTGRES_DB=wallet_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

PGADMIN_DEFAULT_EMAIL=admin@wallet.com
PGADMIN_DEFAULT_PASSWORD=admin
PGADMIN_CONFIG_SERVER_MODE=False
```

### Назначение переменных

- `POSTGRES_USER` - пользователь PostgreSQL
- `POSTGRES_PASSWORD` - пароль PostgreSQL
- `POSTGRES_DB` - основная база приложения
- `POSTGRES_HOST` - хост базы, для Docker это `db`, для локального запуска обычно `localhost`
- `POSTGRES_PORT` - порт PostgreSQL
- `PGADMIN_DEFAULT_EMAIL` - логин для pgAdmin
- `PGADMIN_DEFAULT_PASSWORD` - пароль для pgAdmin
- `PGADMIN_CONFIG_SERVER_MODE` - режим pgAdmin

## Запуск в Docker

### 1. Собрать и поднять контейнеры

```bash
docker compose up --build
```

Что происходит при старте `app`:

1. создаётся тестовая база `wallet_test_db`, если её нет
2. применяются миграции `alembic upgrade head`
3. запускаются тесты `pytest -q tests`
4. стартует `uvicorn`

### 2. Адреса сервисов

- приложение: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- pgAdmin: `http://localhost:5050`

### 3. Настройка pgAdmin

Логин:

- `admin@wallet.com`

Пароль:

- `admin`

Подключение к PostgreSQL:

- Host name/address: `db`
- Port: `5432`
- Maintenance database: `wallet_db`
- Username: `wallet_user`
- Password: `wallet_password`

## Запуск локально

### 1. Установить зависимости

```bash
uv sync
```

Если нужно установить и dev-зависимости:

```bash
uv sync --all-groups
```

### 2. Поднять PostgreSQL

Нужно, чтобы PostgreSQL был доступен по данным из `app/.env`.

### 3. Применить миграции

```bash
uv run alembic upgrade head
```

### 4. Запустить приложение

```bash
uv run uvicorn app.main:app --reload
```

После запуска API будет доступен по адресу:

- `http://127.0.0.1:8000`

Документация Swagger:

- `http://127.0.0.1:8000/docs`

Redoc:

- `http://127.0.0.1:8000/redoc`


## Тесты

Тесты лежат в директории `tests/`.

### Запуск локально

```bash
uv run pytest -q tests
```

### Что проверяют тесты

- создание кошелька
- получение баланса
- пополнение кошелька
- ошибку при попытке снять больше, чем есть
- конкурентные депозиты на один и тот же кошелек

### Тестовая база

Тесты используют отдельную базу:

- `wallet_test_db`

Если нужно указать другую базу:

```bash
export TEST_DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/test_db"
uv run pytest -q tests
```

## Линтер и форматтер

### Проверка

```bash
uv run ruff check .
```

### Автоисправление

```bash
uv run ruff check --fix .
```

### Форматирование

```bash
uv run ruff format .
```

### Проверка форматирования без изменений

```bash
uv run ruff format --check .
```

## Миграции

### Применить миграции

```bash
uv run alembic upgrade head
```

### Создать новую миграцию

```bash
uv run alembic revision --autogenerate -m "describe change"
```
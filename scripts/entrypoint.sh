#!/bin/sh
set -eu

: "${POSTGRES_HOST:=db}"
: "${POSTGRES_PORT:=5432}"
: "${POSTGRES_USER:=wallet_user}"
: "${POSTGRES_PASSWORD:=wallet_password}"
: "${POSTGRES_DB:=wallet_db}"
: "${TEST_POSTGRES_DB:=wallet_test_db}"

export POSTGRES_HOST POSTGRES_PORT POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB
export DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}}"
export TEST_DATABASE_URL="${TEST_DATABASE_URL:-postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${TEST_POSTGRES_DB}}"

python scripts/ensure_test_db.py
alembic upgrade head
pytest -q tests

exec uvicorn app.main:app --host 0.0.0.0 --port 8000

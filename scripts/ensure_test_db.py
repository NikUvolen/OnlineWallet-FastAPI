import asyncio
import os
import re

import asyncpg

DB_NAME_RE = re.compile(r'^[A-Za-z0-9_]+$')


def getenv(name: str, default: str) -> str:
    return os.getenv(name, default)


async def main() -> None:
    host = getenv('POSTGRES_HOST', 'db')
    port = int(getenv('POSTGRES_PORT', '5432'))
    user = getenv('POSTGRES_USER', 'wallet_user')
    password = getenv('POSTGRES_PASSWORD', 'wallet_password')
    test_db = getenv('TEST_POSTGRES_DB', 'wallet_test_db')

    if not DB_NAME_RE.match(test_db):
        raise SystemExit(f'Invalid TEST_POSTGRES_DB value: {test_db!r}')

    connection = None
    for _ in range(30):
        try:
            connection = await asyncpg.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database='postgres',
            )
            break
        except Exception:
            await asyncio.sleep(2)

    if connection is None:
        raise SystemExit('Database is not available')

    try:
        exists = await connection.fetchval(
            'SELECT 1 FROM pg_database WHERE datname = $1',
            test_db,
        )
        if not exists:
            await connection.execute(f'CREATE DATABASE "{test_db}"')
    finally:
        await connection.close()


if __name__ == '__main__':
    asyncio.run(main())

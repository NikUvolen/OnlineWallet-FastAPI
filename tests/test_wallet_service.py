import asyncio
from asyncio import Event, Lock
from decimal import Decimal
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.wallets import service
from app.wallets.models import Wallet
from app.wallets.schemas import OperationType, WalletOperation

pytestmark = pytest.mark.asyncio


async def create_wallet_row(session: AsyncSession) -> Wallet:
    wallet = Wallet()
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)
    return wallet


async def test_create_wallet_returns_zero_balance(session_factory):
    async with session_factory() as session:
        wallet = await service.create_wallet(session)
        await session.commit()

        assert isinstance(wallet.id, UUID)
        assert wallet.balance == Decimal('0.00')


async def test_get_balance_returns_wallet_response(session_factory):
    async with session_factory() as session:
        created = await create_wallet_row(session)

    async with session_factory() as session:
        wallet = await service.get_balance(session, created.id)

        assert wallet.id == created.id
        assert wallet.balance == Decimal('0.00')


async def test_deposit_increases_balance(session_factory):
    async with session_factory() as session:
        created = await create_wallet_row(session)

    operation = WalletOperation(
        operation_type=OperationType.DEPOSIT,
        amount=Decimal('100.04'),
    )

    async with session_factory() as session:
        wallet = await service.update_balance(session, created.id, operation)
        await session.commit()
        await session.refresh(wallet)

        assert wallet.balance == Decimal('100.04')

    async with session_factory() as session:
        updated = await service.get_balance(session, created.id)
        assert updated.balance == Decimal('100.04')


async def test_withdraw_too_much_raises(session_factory):
    async with session_factory() as session:
        created = await create_wallet_row(session)

    operation = WalletOperation(
        operation_type=OperationType.WITHDRAWAL,
        amount=Decimal('1.00'),
    )

    async with session_factory() as session:
        with pytest.raises(ValueError, match='Insufficient balance'):
            await service.update_balance(session, created.id, operation)


async def test_concurrent_deposits_are_not_lost(session_factory):
    async with session_factory() as session:
        created = await create_wallet_row(session)

    workers = 10
    deposit_amount = Decimal('10.04')
    ready_count = 0
    ready_lock = Lock()
    start = Event()

    async def worker() -> None:
        nonlocal ready_count
        async with session_factory() as session:
            async with ready_lock:
                ready_count += 1
                if ready_count == workers:
                    start.set()
            await start.wait()
            wallet = await service.update_balance(
                session,
                created.id,
                WalletOperation(
                    operation_type=OperationType.DEPOSIT,
                    amount=deposit_amount,
                ),
            )
            await session.commit()
            assert wallet.balance >= deposit_amount

    await asyncio.gather(*(worker() for _ in range(workers)))

    async with session_factory() as session:
        final_wallet = await service.get_balance(session, created.id)

    assert final_wallet.balance == deposit_amount * workers

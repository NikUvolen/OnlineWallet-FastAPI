from uuid import UUID
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.wallets.models import Wallet
from app.wallets.schemas import (
    WalletOperation, 
    WalletResponse,
    OperationType
)


async def get_balance(
    session: AsyncSession, 
    wallet_id: UUID
) -> WalletResponse:
    """Get the balance wallet"""
    query = select(Wallet).where(Wallet.id == wallet_id)
    result = await session.execute(query)
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise NoResultFound(f"Wallet with id {wallet_id} not found")
    return WalletResponse.model_validate(wallet)

async def update_balance(
    session: AsyncSession, 
    wallet_id: UUID, 
    operation: WalletOperation
) -> Wallet:
    """Update balance wallet"""
    query = (
        select(Wallet)
        .where(Wallet.id == wallet_id)
        .with_for_update()
    )
    result = await session.execute(query)
    wallet = result.scalar_one_or_none()

    if wallet is None:
        raise NoResultFound(f"Wallet with id {wallet_id} not found")
    
    if operation.operation_type == OperationType.DEPOSIT:
        wallet.balance += operation.amount
    elif operation.operation_type == OperationType.WITHDRAWAL:
        if wallet.balance < operation.amount:
            raise ValueError("Insufficient balance for withdrawal")
        wallet.balance -= operation.amount

    await session.flush()

    return wallet

async def create_wallet(session: AsyncSession) -> WalletResponse:
    """Create new wallet"""
    new_wallet = Wallet()
    session.add(new_wallet)
    await session.flush()
    return WalletResponse.model_validate(new_wallet)

from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.wallets.database import get_db
from app.wallets.models import Wallet
from app.wallets import service
from app.wallets.schemas import WalletOperation, WalletResponse


router = APIRouter(
    prefix='/wallets',
    tags=['wallets']
)


@router.get('/{wallet_id}', response_model=WalletResponse)
async def get_wallet_balance(
    wallet_id: UUID, 
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    """Get the balance of a wallet by its ID."""
    try:
        wallet = await service.get_balance(db, wallet_id)
        return wallet
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Wallet with id {wallet_id} not found'
        )

@router.post('/{wallet_id}/operation', response_model=WalletResponse)
async def update_wallet_balance(
    wallet_id: UUID, 
    operation: WalletOperation, 
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    """Update the balance of a wallet by its ID."""
    try:
        wallet = await service.update_balance(db, wallet_id, operation)
        await db.commit()
        await db.refresh(wallet)
        return WalletResponse.model_validate(wallet)
    except NoResultFound:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Wallet with id {wallet_id} not found'
        )
    except ValueError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An unexpected error occurred'
        )

@router.post(
    '/', 
    response_model=WalletResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_wallet(
    db: AsyncSession = Depends(get_db)
) -> WalletResponse:
    try:
        new_wallet = await service.create_wallet(db)
        await db.commit()
        return new_wallet
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='An unexpected error occurred'
        )

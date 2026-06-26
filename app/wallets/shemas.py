import uuid
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class OperationType(str, Enum):
    DEPOSIT = 'DEPOSIT'
    WITHDRAWAL = 'WITHDRAWAL'


class WalletOperation(BaseModel):
    operation_type: OperationType = Field(
        ..., 
        description='Type of the operation'
    )
    amount: Decimal = Field(
        ...,
        description='Amount of the operation',
        gt=Decimal('0.00'),
        max_digits=10,
        decimal_places=2
    )


class WalletResponse(BaseModel):
    id: uuid.UUID = Field(
        ..., 
        description='Unique identifier of the wallet'
    )
    balance: Decimal = Field(
        ..., 
        description='Current balance of the wallet',
        max_digits=10,
        decimal_places=2
    )

    model_config = {
        'from_attributes': True
    }

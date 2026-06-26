import uuid
from decimal import Decimal
from sqlalchemy import Numeric, UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2), 
        default=Decimal("0.00")
    )
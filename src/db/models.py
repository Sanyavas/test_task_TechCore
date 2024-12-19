from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String())
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, unique=True)  # Використано Numeric для ціни
    external_id: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())

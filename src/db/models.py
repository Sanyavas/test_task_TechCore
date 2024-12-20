from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, Numeric, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String())
    description: Mapped[str] = mapped_column(String())
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, unique=False)
    external_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column('updated_at', DateTime, default=func.now(), onupdate=func.now())

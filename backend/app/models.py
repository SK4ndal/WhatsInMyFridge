from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Foodstuff(Base):
    __tablename__ = "foodstuffs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False, unique=True, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    expiry_min_days: Mapped[int] = mapped_column(Integer, nullable=False)
    expiry_max_days: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="foodstuff")


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    foodstuff_id: Mapped[int | None] = mapped_column(ForeignKey("foodstuffs.id"), nullable=True, index=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    quantity_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity_unit: Mapped[str] = mapped_column(String(40), nullable=False)
    purchase_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    estimated_expiry_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    foodstuff: Mapped[Foodstuff | None] = relationship(back_populates="inventory_items")

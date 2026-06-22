from datetime import date, timedelta
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FoodstuffBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    category: str = Field(min_length=1, max_length=80)
    expiry_min_days: int = Field(ge=0)
    expiry_max_days: int = Field(ge=0)
    notes: str | None = None

    @model_validator(mode="after")
    def validate_expiry_range(self) -> "FoodstuffBase":
        if self.expiry_max_days < self.expiry_min_days:
            raise ValueError("expiry_max_days must be greater than or equal to expiry_min_days")
        return self


class FoodstuffCreate(FoodstuffBase):
    pass


class FoodstuffRead(FoodstuffBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class InventoryItemBase(BaseModel):
    foodstuff_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    quantity_amount: Decimal = Field(gt=0, decimal_places=2)
    quantity_unit: str = Field(min_length=1, max_length=40)
    purchase_date: date
    estimated_expiry_date: date | None = None


class InventoryItemCreate(InventoryItemBase):
    @model_validator(mode="after")
    def require_manual_details_without_foodstuff(self) -> "InventoryItemCreate":
        if self.foodstuff_id is None and (self.name is None or self.category is None or self.estimated_expiry_date is None):
            raise ValueError(
                "name, category, and estimated_expiry_date are required when no foodstuff_id is provided"
            )
        return self


class InventoryItemUpdate(BaseModel):
    foodstuff_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    quantity_amount: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    quantity_unit: str | None = Field(default=None, min_length=1, max_length=40)
    purchase_date: date | None = None
    estimated_expiry_date: date | None = None


class InventoryItemRead(BaseModel):
    id: int
    foodstuff_id: int | None
    name: str
    category: str
    quantity_amount: Decimal
    quantity_unit: str
    purchase_date: date
    estimated_expiry_date: date
    is_active: bool
    foodstuff: FoodstuffRead | None = None

    model_config = ConfigDict(from_attributes=True)


class CategoryGroup(BaseModel):
    category: str
    items: list[InventoryItemRead]


def estimated_expiry_from_foodstuff(purchase_date: date, expiry_max_days: int) -> date:
    return purchase_date + timedelta(days=expiry_max_days)

from decimal import Decimal
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class CustomerBase(SQLModel):
    name: str

class Customer(CustomerBase, table=True):
    id: int = Field(default=None, primary_key=True)
    time_series: List["TimeSeries"] = Relationship(back_populates="customer")

class SIPXPriceBase(SQLModel):
    timestamp: str
    price_eur_kwh: Decimal

class SIPXPrice(SIPXPriceBase, table=True):
    id: int = Field(default=None, primary_key=True)

class TimeSeriesBase(SQLModel):
    timestamp: str
    consumption_kwh: Optional[Decimal] = None
    production_kwh: Optional[Decimal] = None

class TimeSeries(TimeSeriesBase, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    sipx_price_id: Optional[int] = Field(default=None, foreign_key="sipxprice.id")

    customer: Customer = Relationship(back_populates="time_series")
    sipx_price: Optional[SIPXPrice] = Relationship()

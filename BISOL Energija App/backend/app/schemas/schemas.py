from decimal import Decimal
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Pydantic models for Customer
class CustomerBase(BaseModel):
    name: str

class CustomerCreate(CustomerBase):
    pass

class CustomerRead(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# Pydantic models for SIPXPrice
class SIPXPriceBase(BaseModel):
    timestamp: str
    price_eur_kwh: Decimal

class SIPXPriceCreate(SIPXPriceBase):
    pass

class SIPXPriceRead(SIPXPriceBase):
    id: int

    class Config:
        orm_mode = True

# Pydantic models for TimeSeries
class TimeSeriesBase(BaseModel):
    timestamp: str
    consumption_kwh: Optional[Decimal] = None
    production_kwh: Optional[Decimal] = None

class TimeSeriesCreate(TimeSeriesBase):
    customer_id: int
    sipx_price_id: Optional[int] = None

class TimeSeriesRead(TimeSeriesBase):
    id: int
    customer_id: int
    sipx_price_id: Optional[int] = None

    class Config:
        orm_mode = True
        

# Naknadno sem dodal autentikacijo
# Model za podatke, ki jih vključujemo v token
class Token(BaseModel):
    access_token: str
    token_type: str

# Model za uporabnika
class User(BaseModel):
    username: str

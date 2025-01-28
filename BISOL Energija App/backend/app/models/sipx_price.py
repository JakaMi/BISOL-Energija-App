# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, List

# from time_series import TimeSeries

# class SIPXPriceBase(SQLModel):
#     timestamp: str
#     price_eur_kwh: float

# class SIPXPriceCreate(SIPXPriceBase):
#     pass

# class SIPXPriceRead(SIPXPriceBase):
#     id: int

#     class Config:
#         orm_mode = True


# class SIPXPrice(SIPXPriceBase, table=True):
#     id: int = Field(default=None, primary_key=True)
#     time_series: List[TimeSeries] = Relationship(back_populates="sipx_price")

    

# # class SIPXPrice(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     timestamp: str
# #     price_eur_kwh: float
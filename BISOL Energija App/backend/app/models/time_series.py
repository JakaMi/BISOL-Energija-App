# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, List
# from sipx_price import SIPXPrice
# from customer import Customer

# class TimeSeriesBase(SQLModel):
#     timestamp: str
#     consumption_kwh: Optional[float] = None
#     production_kwh: Optional[float] = None

# class TimeSeriesCreate(TimeSeriesBase):
#     customer_id: int

# class TimeSeriesRead(TimeSeriesBase):
#     id: int
#     customer_id: int
#     sipx_price_id: Optional[int]

#     class Config:
#         orm_mode = True


# class TimeSeries(TimeSeriesBase, table=True):
#     id: int = Field(default=None, primary_key=True)
#     customer_id: int = Field(foreign_key="customer.id")
#     sipx_price_id: Optional[SIPXPrice] = Field(default=None, foreign_key="sipxprice.id")
    
#     customer: Customer = Relationship(back_populates="time_series")
#     sipx_price: Optional[SIPXPrice] = Relationship(back_populates="time_series")

    

# # class TimeSeries(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     customer_id: int = Field(foreign_key="customer.id")
# #     timestamp: str
# #     consumption_kwh: Optional[float]
# #     production_kwh: Optional[float]
# #     customer: Customer = Relationship(back_populates="time_series")
# #     sipx_price: Optional[SIPXPrice] = Field(default=None, foreign_key="sipxprice.timestamp")
# #     # customer: "Customer" = Relationship(back_populates="time_series")
# #     # sipx_price: Optional["SIPXPrice"] = Field(default=None, foreign_key="sipxprice.timestamp")
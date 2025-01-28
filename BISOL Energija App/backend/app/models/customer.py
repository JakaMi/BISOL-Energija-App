# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional, List
# from time_series import TimeSeries

# from enum import Enum

# class CustomerType(str, Enum):
#     consumer = "consumer"
#     producer = "producer"
#     both = "both"


# class CustomerBase(SQLModel):
#     name: str
#     customer_type: CustomerType

# class CustomerCreate(CustomerBase):
#     pass

# class CustomerRead(CustomerBase):
#     id: int

#     class Config:
#         orm_mode = True
        
# class Customer(CustomerBase, table=True):
#     id: int = Field(default=None, primary_key=True)
#     time_series: List[TimeSeries] = Relationship(back_populates="customer")

# # class Customer(SQLModel, table=True):
# #     id: Optional[int] = Field(default=None, primary_key=True)
# #     name: str
# #     customer_type: str = Field(default="consumer")  # Values: "consumer", "producer", "both"
# #     time_series: List[TimeSeries] = Relationship(back_populates="customer")
# #     # time_series: List["TimeSeries"] = Relationship(back_populates="customer")
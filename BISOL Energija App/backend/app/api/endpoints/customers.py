


# Customer Routes

## Create customer
from fastapi import Depends, HTTPException
from sqlmodel import Session
from app.auth.auth import get_current_user
from app.db.database import get_db
from app.models.models import Customer
from app.schemas.schemas import CustomerCreate, CustomerRead, User
from app.main import app
from backend.app.crud import get_customer_by_id, get_total_consumption_for_customer, get_total_production_for_customer


# @app.post("/customers/", response_model=CustomerRead)
# def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_customer = Customer(name=customer.name)
#     db.add(db_customer)
#     db.commit()
#     db.refresh(db_customer)
#     return db_customer

# ## Read customers
# @app.get("/customers/", response_model=list[CustomerRead])
# def read_customers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     customers = db.query(Customer).offset(skip).limit(limit).all()
#     return customers

# ## Update customer
# @app.put("/customers/{customer_id}", response_model=CustomerRead)
# def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
#     db_customer = get_customer_by_id(customer_id, db)
    
#     if not db_customer:
#         raise HTTPException(status_code=404, detail="Customer not found")
    
#     db_customer.name = customer.name
#     db.commit()
#     db.refresh(db_customer)
    
#     return db_customer

# ## Delete customer
# @app.delete("/customers/{customer_id}", response_model=CustomerRead)
# async def delete_customer(customer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
#     customer = get_customer_by_id(customer_id, db)
    
#     if not customer:
#         raise HTTPException(status_code=404, detail="Customer not found")
    
#     # Deleting the customer (related TimeSeries will be deleted automatically)
#     db.delete(customer)
#     db.commit()
    
#     return customer

# ## Get Customer
# @app.get("/customers/{customer_id}", response_model=CustomerRead)
# def read_customer(customer_id: int, db: Session = Depends(get_db)):
#     db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
#     if db_customer is None:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return db_customer

# ## Get Customer Production
# @app.get("/customers/{customer_id}/production")
# def get_customer_production(customer_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
#     customer = session.query(Customer).filter(Customer.id == customer_id).first()
#     if not customer:
#         raise HTTPException(status_code=404, detail="Customer not found")

    
#     total_production = get_total_production_for_customer(customer_id, session)
#     return {"customer_id": customer_id, "total_production_kwh": total_production}

# ## Get Customer Consumption
# @app.get("/customers/{customer_id}/consumption")
# def get_customer_consumption(customer_id: int, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     # Check if the customer exists
#     customer = session.query(Customer).filter(Customer.id == customer_id).first()
#     if not customer:
#         raise HTTPException(status_code=404, detail="Customer not found")

#     # Get the total consumption for the customer
#     total_consumption = get_total_consumption_for_customer(customer_id, session)
#     return {"customer_id": customer_id, "total_consumption_kwh": total_consumption}

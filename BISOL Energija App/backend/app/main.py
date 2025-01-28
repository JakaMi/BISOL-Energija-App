from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.auth import create_access_token, get_current_user
from crud import find_all_timeseries_for_customer, get_customer_by_id, get_overview_for_customer_in_timespan, get_total_consumption_for_customer, get_total_consumption_for_customer_in_timespan, get_total_production_for_customer, get_total_production_for_customer_in_timespan, get_overview_for_customer
from db.database import create_db, get_db
from models.models import Customer, TimeSeries, SIPXPrice
from schemas.schemas import CustomerCreate, CustomerRead, TimeSeriesCreate, TimeSeriesRead, SIPXPriceCreate, SIPXPriceRead, Token, User

app = FastAPI()

create_db()


def validate_date_strings(datetime_from: str, datetime_to: str) -> tuple[datetime, datetime]:
    if datetime_from is None or datetime_to is None:
        return None, None
    
    # cast to datetime from string format: 2023-12-31 23:00:00+00:00, 
    datetime_from = datetime.strptime(datetime_from, "%Y-%m-%d %H:%M:%S%z")
    datetime_to = datetime.strptime(datetime_to, "%Y-%m-%d %H:%M:%S%z")
    
    if datetime_from is None or datetime_to is None:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    if datetime_from > datetime_to:
        raise HTTPException(status_code=400, detail="Invalid date range")
    
    return datetime_from, datetime_to

# Authentication
# Naknadno sem dodal autentikacijo, drugače bi bili uporabniki z zakodiranimi gesli shranjeni v bazi
def verify_user_credentials(username: str, password: str) -> bool:
    if username == "testuser" and password == "testpassword":
        return True
    return False

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    if not verify_user_credentials(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/protected-data/")
# async def get_protected_data(current_user: User = Depends(get_current_user)):
#     return {"message": f"Hello, {current_user.username}! You have access to this protected data."}

## Create customer
@app.post("/customers/", response_model=CustomerRead)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_customer = Customer(name=customer.name)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

## Read customers
@app.get("/customers/", response_model=list[CustomerRead])
def read_customers(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):  # vrne 20 strank na stran
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

## Update customer
@app.put("/customers/{customer_id}", response_model=CustomerRead)
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    db_customer = get_customer_by_id(customer_id, db)
    
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_customer.name = customer.name
    db.commit()
    db.refresh(db_customer)
    
    return db_customer

## Delete customer
@app.delete("/customers/{customer_id}", response_model=CustomerRead)
async def delete_customer(customer_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    customer = get_customer_by_id(customer_id, db)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    time_series = find_all_timeseries_for_customer(customer_id, db)
    
    for ts in time_series:
        db.delete(ts)
    db.delete(customer)
    db.commit()
    
    return customer

## Get Customer
@app.get("/customers/{customer_id}", response_model=CustomerRead)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


## Get Customer Production
@app.get("/customers/{customer_id}/production")
def get_customer_production(customer_id: int, datetime_from: str = None, datetime_to: str = None, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    datetime_from, datetime_to = validate_date_strings(datetime_from, datetime_to)
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if datetime_from is None or datetime_to is None:
        # calculate from all time
        total_production_kwh, total_production_price = get_total_production_for_customer(customer_id, session)
        return {"customer_id": customer_id, "total_production_kwh": total_production}
    
    # Get the total production for the customer in the given time range
    total_production_kwh, total_production_price = get_total_production_for_customer_in_timespan(customer_id, datetime_from, datetime_to, session)
    return {"customer_id": customer_id, "total_production_kwh": total_production_kwh, "total_production_price": total_production_price}


## Get Customer Consumption
@app.get("/customers/{customer_id}/consumption")
def get_customer_consumption(customer_id: int, datetime_from: str = None, datetime_to: str = None, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    datetime_from, datetime_to = validate_date_strings(datetime_from, datetime_to)
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if datetime_from is None or datetime_to is None:
        # calculate from all time
        total_consumption_kwh, total_consumption_price = get_total_consumption_for_customer(customer_id, session)
        return {"customer_id": customer_id, "total_consumption_kwh": total_consumption_kwh, "total_consumption_price": total_consumption_price}
    
    # Get the total production for the customer in the given time range
    total_consumption_kwh, total_consumption_price = get_total_consumption_for_customer_in_timespan(customer_id, datetime_from, datetime_to, session)
    return {"customer_id": customer_id, "total_consumption_kwh": total_consumption_kwh, "total_consumption_price": total_consumption_price}

    

## Get Customer Costs
@app.get("/customers/{customer_id}/balance")
def get_customer_balance(customer_id: int, datetime_from: str = None, datetime_to: str = None, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    datetime_from, datetime_to = validate_date_strings(datetime_from, datetime_to)
    
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if datetime_from is None or datetime_to is None:
        # calculate from all time
        total_production_kwh, total_production_cost = get_total_production_for_customer(customer_id, session)
        total_consumption_kwh, total_production_cost = get_total_consumption_for_customer(customer_id, session)
        return {"customer_id": customer_id, "total_production": {"production kwh": total_production_kwh, "cost": total_production_cost}, "total_consumption": {"consumption kwh": total_consumption_kwh, "cost": total_consumption_cost}, "balance": {"production": total_production_kwh - total_consumption_kwh, "cost": total_production_cost - total_consumption_cost}}
    
    # Get the total production for the customer in the given time range
    total_production_kwh, total_production_cost = get_total_production_for_customer_in_timespan(customer_id, datetime_from, datetime_to, session)
    total_consumption_kwh, total_consumption_cost = get_total_consumption_for_customer_in_timespan(customer_id, datetime_from, datetime_to, session)
    
    return {"customer_id": customer_id, "total_production": {"production kwh": total_production_kwh, "cost": total_production_cost}, "total_consumption": {"consumption kwh": total_consumption_kwh, "cost": total_consumption_cost}, "balance": {"production": total_production_kwh - total_consumption_kwh, "cost": total_production_cost - total_consumption_cost}}
        
# # Get Customer Overview
@app.get("/customers/{customer_id}/overview")
def get_customer_overview(customer_id: int, date_from: str = None, date_to: str = None, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    date_from, date_to = validate_date_strings(date_from, date_to)
    
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if date_from is None or date_to is None:
        # calculate from all time
        overview = get_overview_for_customer(customer_id, session)
        return {"customer_id": customer_id, "overview": overview}
    
    # Get the total production for the customer in the given time range
    overview = get_overview_for_customer_in_timespan(customer_id, date_from, date_to, session)
    
    return {"customer_id": customer_id, "overview": overview}
    
# # SIPXPrice Routes
# Create price with timestamp
@app.post("/prices/", response_model=SIPXPriceRead)
def create_price(price: SIPXPriceCreate, db: Session = Depends(get_db)):
    db_price = SIPXPrice(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
    

# # TimeSeries Routes
@app.post("/timeseries/", response_model=TimeSeriesRead)
def create_timeseries(timeseries: TimeSeriesCreate, db: Session = Depends(get_db)):
    db_timeseries = TimeSeries(**timeseries.dict())
    db.add(db_timeseries)
    db.commit()
    db.refresh(db_timeseries)
    return db_timeseries


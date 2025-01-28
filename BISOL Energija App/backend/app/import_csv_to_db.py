import csv
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import engine
from models.models import Customer, SIPXPrice, TimeSeries
from schemas.schemas import CustomerCreate, SIPXPriceCreate, TimeSeriesCreate

with Session(engine) as session:
    # Clear data in tables before re-running
    session.query(Customer).delete()
    session.query(SIPXPrice).delete()
    session.query(TimeSeries).delete()
    session.commit()


def import_csv_to_db(csv_file: str, session: Session):
    # Branje CSV datoteke
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Preverimo ali SIPX cena že obstaja, sicer jo dodamo
            timestamp = row['timestamp_utc']
            sipx_price_value = float(row['SIPX_EUR_kWh'])
            sipx_price = session.query(SIPXPrice).filter(SIPXPrice.timestamp == timestamp).first()

            if not sipx_price:
                # Ustvarimo SIPX ceno, če ne obstaja
                sipx_price_data = SIPXPriceCreate(timestamp=timestamp, price_eur_kwh=sipx_price_value)
                sipx_price = create_sipx_price(session, sipx_price_data)

            # Ustvarimo zapise za vsakega kupca (customer00, customer01, ...)
            for customer_key in range(14):  # Ker imamo 14 strank (customer00, ..., customer13)
                customer_column_consumption = f"customer{customer_key:02d}_cons_kWh"
                customer_column_production = f"customer{customer_key:02d}_prod_kWh"
                
                if customer_column_consumption in row:  # Preverimo, ali obstaja poraba za tega kupca
                    consumption_kwh = float(row.get(customer_column_consumption, 0.0))
                    production_kwh = float(row.get(customer_column_production, 0.0))

                    customer_name = f"customer{customer_key:02d}"
                    print(f"Processing {customer_name}...")

                    # Preverimo ali kupec že obstaja, sicer ga dodamo
                    customer = session.query(Customer).filter(Customer.name == customer_name).first()
                    if not customer:
                        print(f"Adding new customer: {customer_name}")
                        # Ustvarimo novega kupca, če še ne obstaja
                        customer_data = CustomerCreate(name=customer_name)
                        customer = create_customer(session, customer_data)

                    # Ustvarimo zapis za časovno serijo
                    time_series_data = TimeSeriesCreate(
                        timestamp=timestamp,
                        consumption_kwh=consumption_kwh,
                        production_kwh=production_kwh,
                        customer_id=customer.id,
                        sipx_price_id=sipx_price.id
                    )
                    create_time_series(session, time_series_data)

def create_customer(session: Session, customer: CustomerCreate):
    db_customer = Customer.from_orm(customer)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

def create_sipx_price(session: Session, price: SIPXPriceCreate):
    db_price = SIPXPrice.from_orm(price)
    session.add(db_price)
    session.commit()
    session.refresh(db_price)
    return db_price

def create_time_series(session: Session, time_series: TimeSeriesCreate):
    db_time_series = TimeSeries.from_orm(time_series)
    session.add(db_time_series)
    session.commit()
    session.refresh(db_time_series)
    return db_time_series

# Primer uporabe:
if __name__ == "__main__":
    # Povežemo se na bazo
    with Session(engine) as session:
        # Kličemo funkcijo za nalaganje podatkov iz CSV-ja
        import_csv_to_db('./20240101_20241231_historical_cons_prod_and_prices.csv', session)


import pandas as pd
from sqlmodel import Session
from models.models import Customer, SIPXPrice, TimeSeries
from db.database import engine

# Start a session
with Session(engine) as session:
    # Clear data in tables before re-running
    session.query(Customer).delete()
    session.query(SIPXPrice).delete()
    session.query(TimeSeries).delete()
    session.commit()

print("All tables have been cleared.")

# Load the CSV file
csv_file_path = "./20240101_20241231_historical_cons_prod_and_prices.csv"
data = pd.read_csv(csv_file_path)

# Database session
# session = Session(engine)

# Extract unique customers from the column headers
customer_columns = [col for col in data.columns if "_cons_kWh" in col or "_prod_kWh" in col]
unique_customers = set(col.split("_")[0] for col in customer_columns)

# Populate the Customer table
for customer_name in unique_customers:
    existing_customer = session.query(Customer).filter_by(name=customer_name).first()
    if not existing_customer:
        new_customer = Customer(name=customer_name)
        session.add(new_customer)

session.commit()

# Verify customers are added
print(f"Added customers: {[customer.name for customer in session.query(Customer).all()]}")

# Populate the SIPXPrice and TimeSeries tables
for _, row in data.iterrows():
    # Add SIPXPrice
    sipx_price = session.query(SIPXPrice).filter_by(timestamp=row['timestamp_utc']).first()
    if not sipx_price:
        sipx_price = SIPXPrice(
            timestamp=row['timestamp_utc'],
            price_eur_kwh=row['SIPX_EUR_kWh']
        )
        session.add(sipx_price)
        session.commit()

    # Add TimeSeries for each customer
    for customer_name in unique_customers:
        customer = session.query(Customer).filter_by(name=customer_name).first()

        consumption_col = f"{customer_name}_cons_kWh"
        production_col = f"{customer_name}_prod_kWh"

        # Check if columns exist and extract values
        consumption = row.get(consumption_col, None)
        production = row.get(production_col, None)

        if pd.notna(consumption) or pd.notna(production):
            new_time_series = TimeSeries(
                timestamp=row['timestamp_utc'],
                consumption_kwh=consumption if pd.notna(consumption) else None,
                production_kwh=production if pd.notna(production) else None,
                customer_id=customer.id,
                sipx_price_id=sipx_price.id
            )
            session.add(new_time_series)

# Commit all TimeSeries additions
session.commit()
session.close()

print("Database population complete.")
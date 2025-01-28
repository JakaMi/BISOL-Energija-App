import csv
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from backend.app.models import Timestamp, Customer, CustomerData, MarketPrice

# Funkcije za nalaganje podatkov v bazo
def load_data_from_csv(csv_path):
    db = SessionLocal()
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Dodaj časovni žig
                timestamp_obj = db.query(Timestamp).filter_by(timestamp=row["timestamp_utc"]).first()
                if not timestamp_obj:
                    timestamp_obj = Timestamp(timestamp=row["timestamp_utc"])
                    db.add(timestamp_obj)
                    db.commit()
                    db.refresh(timestamp_obj)

                # Dodaj podatke za stranke
                for customer_id in range(10):  # customer00, customer01, ..., customer09
                    customer_name = f"customer{str(customer_id).zfill(2)}"
                    role = "both"  # Predpostavka, da je stranka tako proizvajalec kot potrošnik
                    customer_obj = db.query(Customer).filter_by(name=customer_name).first()
                    if not customer_obj:
                        customer_obj = Customer(name=customer_name, role=role)
                        db.add(customer_obj)
                        db.commit()
                        db.refresh(customer_obj)

                    # Dodaj podatke o porabi/proizvodnji
                    consumption_kwh = float(row.get(f"{customer_name}_cons_kWh", 0))
                    production_kwh = float(row.get(f"{customer_name}_prod_kWh", 0))
                    customer_data = CustomerData(
                        timestamp_id=timestamp_obj.id,
                        customer_id=customer_obj.id,
                        consumption_kwh=consumption_kwh,
                        production_kwh=production_kwh
                    )
                    db.add(customer_data)

                # Dodaj SIPX ceno
                sipx_price = float(row["SIPX_EUR_kWh"])
                market_price = MarketPrice(
                    timestamp_id=timestamp_obj.id,
                    price_eur_kwh=sipx_price
                )
                db.add(market_price)

            # Shrani vse v bazo
            db.commit()
            print("Podatki so uspešno naloženi v bazo!")
    except Exception as e:
        db.rollback()
        print(f"Napaka pri nalaganju podatkov: {e}")
    finally:
        db.close()

# Pot do vaše datoteke CSV
if __name__ == "__main__":
    CSV_FILE_PATH = "../app/db/20240101_20241231_historical_cons_prod_and_prices.csv"
    load_data_from_csv(CSV_FILE_PATH)

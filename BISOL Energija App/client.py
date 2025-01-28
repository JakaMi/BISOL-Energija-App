import requests
from datetime import datetime

# Osnovna konfiguracija
BASE_URL = "http://localhost:8000"  # Zamenjaj s pravo URL
USERNAME = "testuser"
PASSWORD = "testpassword"

class APIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = self.authenticate()

    def authenticate(self):
        url = f"{self.base_url}/token"
        response = requests.post(url, data={"username": self.username, "password": self.password})
        if response.status_code != 200:
            raise Exception(f"Authentication failed: {response.json()}")
        return response.json()["access_token"]

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def create_customer(self, name):
        url = f"{self.base_url}/customers/"
        payload = {"name": name}
        response = requests.post(url, json=payload, headers=self.headers())
        return response.json()

    def get_customer(self, customer_id):
        url = f"{self.base_url}/customers/{customer_id}"
        response = requests.get(url, headers=self.headers())
        return response.json()

    def update_customer(self, customer_id, name):
        url = f"{self.base_url}/customers/{customer_id}"
        payload = {"name": name}
        response = requests.put(url, json=payload, headers=self.headers())
        return response.json()

    def delete_customer(self, customer_id):
        url = f"{self.base_url}/customers/{customer_id}"
        response = requests.delete(url, headers=self.headers())
        return response.json()

    def get_customer_production(self, customer_id, datetime_from=None, datetime_to=None):
        url = f"{self.base_url}/customers/{customer_id}/production"
        params = {"datetime_from": datetime_from, "datetime_to": datetime_to}
        response = requests.get(url, headers=self.headers(), params=params)
        return response.json()

    def get_customer_consumption(self, customer_id, datetime_from=None, datetime_to=None):
        url = f"{self.base_url}/customers/{customer_id}/consumption"
        params = {"datetime_from": datetime_from, "datetime_to": datetime_to}
        response = requests.get(url, headers=self.headers(), params=params)
        return response.json()

    def get_customer_balance(self, customer_id, datetime_from=None, datetime_to=None):
        url = f"{self.base_url}/customers/{customer_id}/balance"
        params = {"datetime_from": datetime_from, "datetime_to": datetime_to}
        response = requests.get(url, headers=self.headers(), params=params)
        return response.json()

    def get_customer_overview(self, customer_id, datetime_from=None, datetime_to=None):
        url = f"{self.base_url}/customers/{customer_id}/overview"
        params = {"datetime_from": datetime_from, "datetime_to": datetime_to}
        response = requests.get(url, headers=self.headers(), params=params)
        return response.json()

    def create_timeseries(self, customer_id, timestamp, production_kwh, consumption_kwh, price_id):
        url = f"{self.base_url}/timeseries/"
        payload = {
            "customer_id": customer_id,
            "timestamp": timestamp,
            "production_kwh": production_kwh,
            "consumption_kwh": consumption_kwh,
            "sipx_price_id": price_id
        }
        response = requests.post(url, json=payload, headers=self.headers())
        return response.json()

    def create_price(self, timestamp, price_eur_kwh):
        url = f"{self.base_url}/prices/"
        payload = {"timestamp": timestamp, "price_eur_kwh": price_eur_kwh}
        response = requests.post(url, json=payload, headers=self.headers())
        return response.json()


# Primer uporabe klienta
if __name__ == "__main__":
    client = APIClient(BASE_URL, USERNAME, PASSWORD)
    customerId = 3
    # from 2023-12-31 23:00:00+00:00
    datetime_from = "2023-12-31 23:00:00+00:00"
    # to 2024-01-01 19:00:00+00:00
    datetime_to = "2024-01-01 19:00:00+00:00"
    
    # 0. Pridobi token
    print("Pridobivanje tokena...")
    print("/token")
    client.headers()
    print("Token pridobljen.")
    print()
    input("Press Enter to continue...")
    print()
    
    # 1. Ustvari stranko
    print("Ustvarjanje nove stranke...")
    print("/customers/")
    new_customer = client.create_customer(name="Test 2 Customer")
    print("Ustvarjena stranka:", new_customer)
    print()
    input("Press Enter to continue...")
    print()

    # 2. Pridobi stranko
    print("Pridobivanje stranke...")
    print("/customers/{customer_id}")
    customer = client.get_customer(customer_id=customerId)
    print("Pridobljena stranka:", customer)
    print()
    input("Press Enter to continue...")
    print()

    # 3. Posodobi stranko
    print("Posodabljanje stranke...")
    print("/customers/{customer_id}")
    updated_customer = client.update_customer(customer_id=new_customer['id'], name="Updated Customer")
    print("Posodobljena stranka:", updated_customer)
    print()
    input("Press Enter to continue...")
    print()

    # 4. Ustvari ceno
    print("Ustvarjanje cene...")
    print("/prices/")
    timestamp = datetime.now().isoformat()
    price = client.create_price(timestamp=timestamp, price_eur_kwh=0.25)
    print("Ustvarjena cena:", price)
    print()
    input("Press Enter to continue...")
    print()

    # 5. Ustvari TimeSeries za stranko
    print("Ustvarjanje TimeSeries za stranko...")
    print("/timeseries/")
    timeseries = client.create_timeseries(
        customer_id=new_customer["id"],
        timestamp=timestamp,
        production_kwh=100.5,
        consumption_kwh=50.3,
        price_id=price["id"]
    )
    print("Ustvarjen TimeSeries:", timeseries)
    print()
    input("Press Enter to continue...")
    print()

    # 6. Pridobi proizvodnjo stranke
    print("Pridobivanje proizvodnje stranke...")
    print("/customers/{customer_id}/production")
    production = client.get_customer_production(customer_id=customerId, datetime_from=datetime_from, datetime_to=datetime_to)
    print("Proizvodnja stranke:", production)
    print()
    input("Press Enter to continue...")
    print()
    
    # 7. Pridobi porabo stranke
    print("Pridobivanje porabe stranke...")
    print("/customers/{customer_id}/consumption")
    consumption = client.get_customer_consumption(customer_id=customerId, datetime_from=datetime_from, datetime_to=datetime_to)
    print("Poraba stranke:", consumption)
    print()
    input("Press Enter to continue...")
    print()
    
    # 8. Pridobi stanje stranke
    print("Pridobivanje stanja stranke...")
    print("/customers/{customer_id}/balance")
    balance = client.get_customer_balance(customer_id=customerId, datetime_from=datetime_from, datetime_to=datetime_to)
    print("Stanje stranke:", balance)
    print()
    input("Press Enter to continue...")
    print()
    
    # 9. Pridobi pregled stranke
    print("Pridobivanje pregleda stranke...")
    print("/customers/{customer_id}/overview")
    overview = client.get_customer_overview(customer_id=customerId, datetime_from=datetime_from, datetime_to=datetime_to)
    print("Pregled stranke:", overview)
    print()
    input("Press Enter to continue...")
    print()
    

    # 7. Izbriši stranko
    print("Brisanje stranke...")
    print("/customers/{customer_id}")
    deleted_customer = client.delete_customer(customer_id=new_customer["id"])
    print("Izbrisana stranka:", deleted_customer)
    print()
    input("Press Enter to continue...")
    print()

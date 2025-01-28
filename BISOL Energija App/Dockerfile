# Uporabi uradno Python bazo
FROM python:3.10-slim

# Nastavi delovni direktorij
WORKDIR /app

# Kopiraj odvisnosti v kontejner
COPY requirements.txt .

# Namesti odvisnosti
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj aplikacijo v kontejner
COPY . .

# Poskrbi, da bo baza vidna
VOLUME /app/data

# Eksponiraj vrata za API
EXPOSE 8000

# Ukaz za zagon aplikacije
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

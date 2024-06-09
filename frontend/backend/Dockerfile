# Użyj oficjalnego obrazu Pythona jako bazy
FROM python:3.8-slim-buster

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . /app

# Zainstaluj wymagane zależności
RUN pip install --no-cache-dir -r requirements.txt

# Uruchom skrypt scraper.py
CMD ["python", "scraper.py"]

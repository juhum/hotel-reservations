import json
import yaml
from pymongo import MongoClient

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB configuration from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Establish connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Pobierz dane z kolekcji
hotels = list(db.hotels.find({}, {'_id': 0}))
guests = list(db.guests.find({}, {'_id': 0}))
reservations = list(db.reservations.find({}, {'_id': 0}))

# Zbiorczy słownik
data = {
    "hotels": hotels,
    "guests": guests,
    "reservations": reservations
}

# Eksport do JSON
with open("data/processed/json_export.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

# Eksport do YAML
with open("data/processed/yaml_export.yaml", "w", encoding="utf-8") as yaml_file:
    yaml.dump(data, yaml_file, allow_unicode=True, sort_keys=False)

print("✅ Eksport do JSON i YAML zakończony.")

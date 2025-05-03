import json
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


# Kolekcje
hotels_collection = db["hotels"]
guests_collection = db["guests"]
reservations_collection = db["reservations"]

# Wczytanie danych JSON z pliku
with open("data/processed/json_output.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Czyszczenie kolekcji (opcjonalne)
hotels_collection.delete_many({})
guests_collection.delete_many({})
reservations_collection.delete_many({})

# Import danych
hotels_collection.insert_many(data["hotels"])
guests_collection.insert_many(data["guests"])
reservations_collection.insert_many(data["reservations"])

print("✅ Import zakończony pomyślnie.")

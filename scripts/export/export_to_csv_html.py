from pymongo import MongoClient
import pandas as pd
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

# ===== Eksport rezerwacji do CSV =====
reservations = list(db["reservations"].find({}, {"_id": 0}))
df_res = pd.DataFrame(reservations)
df_res.to_csv("data/processed/export_reservations.csv", index=False)
print("✅ Eksport rezerwacji do CSV: export_reservations.csv")

# ===== Eksport gości do HTML =====
guests = list(db["guests"].find({}, {"_id": 0}))
df_guests = pd.DataFrame(guests)
df_guests.to_html("data/processed/export_guests.html", index=False)
print("✅ Eksport gości do HTML: export_guests.html")

# ===== Eksport pokoi (wszystkich) do CSV =====
hotels = list(db["hotels"].find({}, {"_id": 0}))
rooms_data = []
for hotel in hotels:
    for room in hotel["rooms"]:
        room["hotel_name"] = hotel["name"]
        room["location"] = hotel["location"]
        rooms_data.append(room)

df_rooms = pd.DataFrame(rooms_data)
df_rooms.to_csv("data/processed/export_rooms.csv", index=False)
print("✅ Eksport pokoi do CSV: export_rooms.csv")

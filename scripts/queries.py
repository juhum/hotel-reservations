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


hotels = db["hotels"]
guests = db["guests"]
reservations = db["reservations"]

# 1. Lista dostępnych pokoi
print("\nDostępne pokoje:")
for hotel in hotels.find():
    print(f"\n🏨 {hotel['name']} ({hotel['location']})")
    for room in hotel.get("rooms", []):
        if room.get("available"):
            print(f"  - Pokój {room['number']} | Typ: {room['type']} | Cena: {room['price']} zł")

# 2. Średnia cena pokoi w hotelach
print("\nŚrednia cena pokoi w hotelach:")
pipeline = [
    {"$unwind": "$rooms"},
    {
        "$group": {
            "_id": "$name",
            "average_price": {"$avg": "$rooms.price"}
        }
    },
    {"$sort": {"_id": 1}}
]
for result in hotels.aggregate(pipeline):
    print(f"{result['_id']}: Średnia cena = {round(result['average_price'], 2)} zł")

# 3. Rezerwacje danego gościa
email = "anna.nowak@example.com"
print(f"\nRezerwacje dla gościa {email}:")
user_reservations = list(reservations.find({"guest_email": email}))
if user_reservations:
    for res in user_reservations:
        print(f"  - Hotel: {res['hotel_name']}, Pokój: {res['room_number']}, Od: {res['check_in']} Do: {res['check_out']}, Status: {res['status']}")
else:
    print("  Brak rezerwacji.")

# 4. Liczba rezerwacji wg statusu
print("\nLiczba rezerwacji wg statusu:")
pipeline = [
    {"$group": {"_id": "$status", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]
for result in reservations.aggregate(pipeline):
    print(f"{result['_id']}: {result['count']} rezerwacji")

# 5. Liczba dostępnych pokoi w każdym hotelu
print("\nDostępność pokoi:")
for hotel in hotels.find():
    available_rooms = [r for r in hotel.get("rooms", []) if r.get("available")]
    print(f"{hotel['name']} – dostępnych pokoi: {len(available_rooms)}")

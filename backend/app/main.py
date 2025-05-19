from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import yaml
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Establish MongoDB connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
hotels_collection = db["hotels"]
guests_collection = db["guests"]
reservations_collection = db["reservations"]

app = FastAPI(title="Hotel Reservations API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Room(BaseModel):
    id: int
    type: str
    price: float
    capacity: int
    description: Optional[str] = None
    amenities: List[str] = []

# Sample data
rooms = [
    Room(
        id=1,
        type="Standard",
        price=100.00,
        capacity=2,
        description="Comfortable room with a queen-size bed",
        amenities=["Wi-Fi", "TV", "Air Conditioning"]
    ),
    Room(
        id=2,
        type="Deluxe",
        price=150.00,
        capacity=2,
        description="Spacious room with a king-size bed and city view",
        amenities=["Wi-Fi", "TV", "Air Conditioning", "Mini Bar", "City View"]
    ),
    Room(
        id=3,
        type="Suite",
        price=250.00,
        capacity=4,
        description="Luxury suite with separate living area",
        amenities=["Wi-Fi", "TV", "Air Conditioning", "Mini Bar", "Living Room", "Kitchen"]
    ),
]

@app.get("/")
async def root():
    return {"message": "Welcome to Hotel Reservations API"}

@app.get("/api/rooms", response_model=List[Room])
async def get_rooms():
    return rooms

@app.get("/api/rooms/{room_id}", response_model=Room)
async def get_room(room_id: int):
    for room in rooms:
        if room.id == room_id:
            return room
    return {"error": "Room not found"}

@app.post("/api/reservations/upload")
async def upload_reservations(file: UploadFile = File(...)):
    try:
        # Read the uploaded YAML file
        content = await file.read()
        yaml_data = yaml.safe_load(content)
        
        # Validate the data structure
        required_sections = ["hotels", "guests", "reservations"]
        for section in required_sections:
            if section not in yaml_data:
                raise HTTPException(status_code=400, detail=f"Missing required section: {section}")
        
        # Clear existing collections
        hotels_collection.delete_many({})
        guests_collection.delete_many({})
        reservations_collection.delete_many({})
        
        # Insert new data
        hotels_collection.insert_many(yaml_data["hotels"])
        guests_collection.insert_many(yaml_data["guests"])
        reservations_collection.insert_many(yaml_data["reservations"])
        
        return {
            "message": "Data uploaded successfully",
            "hotels_count": len(yaml_data["hotels"]),
            "guests_count": len(yaml_data["guests"]),
            "reservations_count": len(yaml_data["reservations"])
        }
        
    except yaml.YAMLError:
        raise HTTPException(status_code=400, detail="Invalid YAML format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
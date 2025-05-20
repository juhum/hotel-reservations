from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from typing import List, Optional
import yaml
import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import tempfile
from datetime import date
import bson
import pandas as pd
import zipfile
import io

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


def convert_dates_to_iso(data):
    """Convert date objects to ISO format strings in the data structure."""
    if isinstance(data, dict):
        return {k: convert_dates_to_iso(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_dates_to_iso(item) for item in data]
    elif isinstance(data, date):
        return data.isoformat()
    return data


@app.get("/")
async def root():
    return {"message": "Welcome to Hotel Reservations API"}


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
        
        # Convert dates to ISO format strings
        yaml_data = convert_dates_to_iso(yaml_data)
        
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


@app.get("/api/data")
async def get_all_data():
    try:
        # Retrieve all data from collections
        hotels = list(hotels_collection.find({}, {'_id': 0}))
        guests = list(guests_collection.find({}, {'_id': 0}))
        reservations = list(reservations_collection.find({}, {'_id': 0}))
        
        return {
            "hotels": hotels,
            "guests": guests,
            "reservations": reservations,
            "counts": {
                "hotels": len(hotels),
                "guests": len(guests),
                "reservations": len(reservations)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/yaml-to-csv")
async def yaml_to_csv(file: UploadFile = File(...)):
    try:
        # Read and parse YAML file
        content = await file.read()
        yaml_data = yaml.safe_load(content.decode('utf-8'))
        
        # Flatten all data into a single list
        all_data = []
        
        # Process hotels and rooms
        if 'hotels' in yaml_data:
            for hotel in yaml_data['hotels']:
                hotel_data = hotel.copy()
                rooms = hotel_data.pop('rooms', [])
                if rooms:
                    for room in rooms:
                        row = {
                            'section': 'hotels',
                            'hotel_name': hotel['name'],
                            'hotel_location': hotel['location'],
                            'hotel_stars': hotel['stars'],
                            'room_number': room['number'],
                            'room_type': room['type'],
                            'room_price': room['price'],
                            'room_available': room['available']
                        }
                        all_data.append(row)
        
        # Process guests
        if 'guests' in yaml_data:
            for guest in yaml_data['guests']:
                row = {
                    'section': 'guests',
                    'first_name': guest.get('first_name', ''),
                    'last_name': guest.get('last_name', ''),
                    'email': guest.get('email', ''),
                    'phone': guest.get('phone', '')
                }
                all_data.append(row)
        
        # Process reservations
        if 'reservations' in yaml_data:
            for reservation in yaml_data['reservations']:
                row = {
                    'section': 'reservations',
                    'guest_email': reservation.get('guest_email', ''),
                    'room_number': reservation.get('room_number', ''),
                    'hotel_name': reservation.get('hotel_name', ''),
                    'start_date': reservation.get('start_date', ''),
                    'end_date': reservation.get('end_date', ''),
                    'status': reservation.get('status', '')
                }
                all_data.append(row)
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data)
        
        # Create CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')
        
        # Return CSV file
        return Response(
            content=output.getvalue().encode('utf-8-sig'),
            media_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename=converted_data.csv'
            }
        )
            
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.post("/api/yaml-to-html")
async def yaml_to_html(file: UploadFile = File(...)):
    try:
        # Read and parse YAML file
        content = await file.read()
        yaml_data = yaml.safe_load(content.decode('utf-8'))
        
        # Start building HTML
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Hotel Data Export</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h2 { color: #333; margin-top: 30px; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f5f5f5; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                tr:hover { background-color: #f0f0f0; }
            </style>
        </head>
        <body>
        """
        
        # Process hotels
        if 'hotels' in yaml_data:
            html_content += "<h2>Hotels and Rooms</h2>"
            html_content += """
            <table>
                <tr>
                    <th>Hotel Name</th>
                    <th>Location</th>
                    <th>Stars</th>
                    <th>Room Number</th>
                    <th>Room Type</th>
                    <th>Price</th>
                    <th>Available</th>
                </tr>
            """
            
            for hotel in yaml_data['hotels']:
                rooms = hotel.get('rooms', [])
                if rooms:
                    for room in rooms:
                        html_content += f"""
                        <tr>
                            <td>{hotel['name']}</td>
                            <td>{hotel['location']}</td>
                            <td>{hotel['stars']}</td>
                            <td>{room['number']}</td>
                            <td>{room['type']}</td>
                            <td>{room['price']}</td>
                            <td>{'Yes' if room['available'] else 'No'}</td>
                        </tr>
                        """
            
            html_content += "</table>"
        
        # Process guests
        if 'guests' in yaml_data:
            html_content += "<h2>Guests</h2>"
            html_content += """
            <table>
                <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                </tr>
            """
            
            for guest in yaml_data['guests']:
                html_content += f"""
                <tr>
                    <td>{guest.get('first_name', '')}</td>
                    <td>{guest.get('last_name', '')}</td>
                    <td>{guest.get('email', '')}</td>
                    <td>{guest.get('phone', '')}</td>
                </tr>
                """
            
            html_content += "</table>"
        
        # Process reservations
        if 'reservations' in yaml_data:
            html_content += "<h2>Reservations</h2>"
            html_content += """
            <table>
                <tr>
                    <th>Guest Email</th>
                    <th>Room Number</th>
                    <th>Hotel Name</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                    <th>Status</th>
                </tr>
            """
            
            for reservation in yaml_data['reservations']:
                html_content += f"""
                <tr>
                    <td>{reservation.get('guest_email', '')}</td>
                    <td>{reservation.get('room_number', '')}</td>
                    <td>{reservation.get('hotel_name', '')}</td>
                    <td>{reservation.get('start_date', '')}</td>
                    <td>{reservation.get('end_date', '')}</td>
                    <td>{reservation.get('status', '')}</td>
                </tr>
                """
            
            html_content += "</table>"
        
        # Close HTML
        html_content += """
        </body>
        </html>
        """
        
        # Return HTML file
        return Response(
            content=html_content,
            media_type='text/html',
            headers={
                'Content-Disposition': 'attachment; filename=converted_data.html'
            }
        )
            
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}") 
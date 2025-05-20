from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv
import sys
from urllib.parse import urlparse

def test_mongodb_connection():
    # Load environment variables
    load_dotenv()
    
    # Get MongoDB configuration
    MONGO_URI = os.getenv("MONGO_URI")

    print(f"MONGO_URI: {MONGO_URI}")
    
    if not MONGO_URI:
        print("❌ Error: MONGO_URI not found in environment variables")
        print("Please check your .env file")
        sys.exit(1)
    
    # Extract database name from URI
    try:
        parsed_uri = urlparse(MONGO_URI)
        DB_NAME = parsed_uri.path[1:]  # Remove leading slash
        if not DB_NAME:
            print("❌ Error: No database name found in MONGO_URI")
            sys.exit(1)
    except Exception as e:
        print("❌ Error: Invalid MONGO_URI format")
        print(f"Error: {str(e)}")
        sys.exit(1)
    
    print(f"DB_NAME: {DB_NAME}")
    
    try:
        # Create a new client and connect to the server
        print("🔄 Attempting to connect to MongoDB...")
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Force a connection to verify it's working
        client.server_info()
        
        # Test database access
        db = client[DB_NAME]
        collections = db.list_collection_names()
        
        print("✅ Successfully connected to MongoDB!")
        print(f"📊 Database: {DB_NAME}")
        print(f"📚 Collections found: {', '.join(collections) if collections else 'No collections found'}")
        
        # Test each collection
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"  - {collection}: {count} documents")
        
    except ConnectionFailure as e:
        print("❌ Failed to connect to MongoDB server")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except ServerSelectionTimeoutError as e:
        print("❌ Server selection timeout")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print("❌ An unexpected error occurred")
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if 'client' in locals():
            client.close()
            print("\n🔌 Connection closed")

if __name__ == "__main__":
    test_mongodb_connection() 
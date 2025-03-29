from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

db = client.daraja_mcp

workflow_collection = db["analyzed_documents"]


def get_analyzed_documents():
    response = workflow_collection.find()
    
    documents = []
    for doc in response:
        documents.append(doc.get("text"))
        
    return documents


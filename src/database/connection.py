import os

from pymongo import MongoClient
from pymongo.database import Database

from src.utils.config import Config

settings = Config()

class DatabaseConnection:
    """
    DatabaseConnection is a singleton class that manages the connection to a MongoDB database.

    Attributes:
        _client (MongoClient): A private class attribute that holds the MongoDB client instance.

    Methods:
        __new__(cls) -> MongoClient:
            Creates and returns a MongoDB client instance if it doesn't already exist.
            Constructs the MongoDB connection URL using settings for database user, password, host, and port.
    """
    _client: MongoClient = None

    def __new__(cls) -> MongoClient:
        url = f'mongodb://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}'
        if cls._client is None:
            cls._client: MongoClient = MongoClient(url)
        return cls._client

def get_database_client():
    client = DatabaseConnection()    
    
    yield client
    

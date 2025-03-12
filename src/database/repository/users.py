import bson.json_util
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

import json
import bson

class UsersRepository:
    """
    A repository class for managing user data in a MongoDB collection.
    Attributes:
        db (MongoClient): The MongoDB client instance.
        collection (str): The name of the collection to interact with.
    Methods:
        __init__(db: MongoClient):
            Initializes the UsersRepository with a MongoDB client instance.
        create(data: dict) -> dict:
            Inserts a new user document into the collection.
            Args:
                data (dict): The user data to insert.
            Returns:
                dict: The inserted user document.
        get_by_email(email: str):
            Retrieves a user document by email.
            Args:
                email (str): The email of the user to retrieve.
            Returns:
                dict: The user document if found, otherwise None.
        get_all():
            Retrieves all user documents from the collection.
            Returns:
                pymongo.cursor.Cursor: A cursor to the documents in the collection.
        update(email: str, data: dict):
            Replaces a user document with the given data.
            Args:
                email (str): The email of the user to update.
                data (dict): The new user data.
            Returns:
                int: The number of documents modified.
        delete(email: str) -> bool:
            Deletes a user document by email.
            Args:
                email (str): The email of the user to delete.
            Returns:
                bool: True if a document was deleted, otherwise False.
    """

    def __init__(self, db_client: MongoClient):
        self.db: Database = db_client.get_database('users')
        self.collection: Collection = self.db.get_collection('users')
    
    def create(self, data: dict) -> dict:
        user = self.collection.insert_one(data)
        if user.acknowledged:
            user = json.loads(bson.json_util.dumps(data))
        return user
    
    def get_by_email(self, email: str):
        user = self.collection.find_one({"email": email})
        if user:
            user = json.loads(bson.json_util.dumps(user))
        return user

    def get_all(self):
        users = self.collection.find()
        serialized_users = json.loads(bson.json_util.dumps(users))
        return serialized_users

    def update(self, email: int, data: dict):
        result = self.collection.replace_one(
            {'email': email},
            data
        )
        return result.upserted_id
    
    def delete(self, email: int) -> bool:
        result = self.collection.delete_one(
            {'email': email}
        )
        serialized_result = json.loads(bson.json_util.dumps(result))
        return serialized_result

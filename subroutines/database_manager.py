from pymongo import MongoClient, errors

import config as CONFIG


class DatabaseManager:
    """
    Handles tasks relating to storing news articles in a MongoDB database.
    """
    def __init__(self):
        try:
            self.client = MongoClient(CONFIG.URI)
            self.db = self.client[CONFIG.DB_NAME]
            self.collection = self.db[CONFIG.DB_COLLECTION]
        except errors.ConnectionFailure as e:
            raise RuntimeError("Failed to connect to MongoDB") from e
        
    def insert_record(self, hash_id:str,
                     title:str,
                     category:str,
                     url:str) -> bool:
        """
        Inserts a new article into database
        Returns True if successful, False if duplicate
        """
        document = {
            "_id": hash_id,    
            "Article Title": title,
            "Category": category,
            "URL": url,
            "Status": CONFIG.STATUS_DEFAULT,
            "Rating": CONFIG.RATING_DEFAULT
        }

        try:
            self.collection.insert_one(document)
            return True
        except errors.DuplicateKeyError:
            return False
        except errors.PyMongoError as e:
            raise RuntimeError("Failed to insert record into MongoDB") from e    
        
    def check_duplicate(self, hash_id:str) -> bool:
        """
        Checks if an article with given hash_id already exists.
        Returns True if duplicate, False otherwise.
        """
        try:
            result = self.collection.find_one({"_id": hash_id})
            return result is not None
        except errors.PyMongoError as e:
            raise RuntimeError("Failed to query MongoDB") from e

    def update_rating(self, hash_id:str, new_rating:int) -> bool:
        """
        Updates the rating of an article. (1 to 5 like stars)
        Returns True if successful, False if article not found.
        """
        try:
            result = self.collection.update_one(
                {"_id": hash_id},
                {"$set": {"Rating": new_rating}}
            )
            return result.matched_count == 1
        except errors.PyMongoError as e:
            raise RuntimeError("Failed to update record in MongoDB") from e

    def get_article(self, hash_id:str) -> dict:
        """
        Retrieves an article by its hash_id.
        Returns the article document or None if not found.
        """
        try:
            document = self.collection.find_one({"_id": hash_id})
            return document
        except errors.PyMongoError as e:
            raise RuntimeError("Failed to retrieve record from MongoDB") from e
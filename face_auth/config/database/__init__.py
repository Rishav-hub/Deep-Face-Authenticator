import pymongo

from face_auth.constant.database_constants import (
    DATABASE_NAME,
    MONGODB_URL_KEY
)


class MongodbClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        if MongodbClient.client is None:
            mongo_db_url = MONGODB_URL_KEY
            if "localhost" in mongo_db_url:
                MongodbClient.client = pymongo.MongoClient(mongo_db_url) 
            else:
                MongodbClient.client=pymongo.MongoClient(mongo_db_url)
        self.client = MongodbClient.client
        self.database = self.client[database_name]
        self.database_name = database_name

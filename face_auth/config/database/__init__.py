import pymongo

from face_auth.constant.database_constants import DATABASE_NAME, ATLAS_CLUSTER_USERNAME,\
        ATLAS_CLUSTER_PASSWORD

class MongodbClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        if MongodbClient.client is None:
           MongodbClient.client= pymongo.MongoClient(
                f"mongodb+srv://{ATLAS_CLUSTER_USERNAME}:{ATLAS_CLUSTER_PASSWORD}@cluster0.tbafllp.mongodb.net/{database_name}?retryWrites=true&w=majority"
                )
        self.client=MongodbClient.client
        self.database = self.client[database_name]
        self.database_name = database_name


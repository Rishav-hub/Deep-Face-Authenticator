from face_auth.constant.database_constants import EMBEDDING_COLLECTION_NAME

# from face_auth.entity.user_embedding import Embedding
from face_auth.config.database import MongodbClient

class UserEmbeddingData:

    def __init__(self) -> None:
        self.client = MongodbClient()
        self.collection_name = EMBEDDING_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user_embedding(self, uuid_: str, embedding_list) -> None:
        self.collection.insert_one({"UUID": uuid_, "user_embed": embedding_list})

    def get_user_embedding(self, uuid_:str) -> dict:
        user:dict = self.collection.find_one({"UUID": uuid_})
        if user != None: 
            return user
        else:
            return None

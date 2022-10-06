from typing import List
from face_auth.constant.database_constants import EMBEDDING_COLLECTION_NAME
from face_auth.data_access.user_data import UserData

from face_auth.entity.user_embedding import Embedding
from face_auth.config.database import MongodbClient

class UserEmbeddingData:

    def __init__(self) -> None:
        self.client = MongodbClient()
        self.collection_name = EMBEDDING_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user_embedding(self, uuid_: str, embedding_list) -> None:
        self.collection.insert_one({"UUID": uuid_, "user_embed": embedding_list})

    def get_user_embedding(self, uuid_:str)->Embedding:
        user:dict = self.collection.find_one({"UUID": uuid_})
        if user != None:
            embedding = Embedding(UUID=user["UUID"], user_embed=user["user_embed"])
            return embedding
        else:
            return None

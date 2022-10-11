from ast import Bytes
import numpy as np
import sys
import io
from typing import List
from PIL import Image

from deepface.commons.functions import detect_face
from deepface import DeepFace
from face_auth.data_access import user_embedding_data

from face_auth.entity.user_embedding import Embedding
from face_auth.data_access.user_embedding_data import UserEmbeddingData
from face_auth.exception import AppException
from face_auth.constant.embedding_constants import SIMILARITY_THRESHOLD

class UserLoginEmbeddingValidation:
    def __init__(self, uuid_: str) -> None:
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()
        self.user = self.user_embedding_data.get_user_embedding(uuid_)

    def validate(self) -> bool:
        try:
            if self.user['UUID'] == None:
                return False
            if self.user['user_embed'] == None:
                return False
            return True
        except Exception as e:
            raise e

    @staticmethod
    def generateEmbedding(img_array: np.ndarray) -> np.ndarray:
        """
        Generate embedding from image array"""
        try:
            faces = detect_face(img_array, detector_backend = 'mtcnn',\
                enforce_detection = False)
            # Generate embedding from face
            embed = DeepFace.represent(img_path = faces[0], model_name = 'Facenet', enforce_detection = False)
            return embed
        except Exception as e:
            raise AppException(e, sys) from e
    
    @staticmethod
    def generateEmbeddingList(files: List[Bytes]) -> List[np.ndarray]:
        """
        Generate embedding list from image array
        """
        embedding_list = []
        for contents in files:
            img = Image.open(io.BytesIO(contents))
            # read image array
            img_array = np.array(img)
            # Detect faces
            embed = UserLoginEmbeddingValidation.generateEmbedding(img_array)
            embedding_list.append(embed)
        return embedding_list

    @staticmethod
    def averageEmbedding(embedding_list: List[np.ndarray]) -> List:
        """_summary_

        Args:
            embedding_list (List[np.ndarray]): _description_

        Returns:
            List: _description_
        
        """
        avg_embed = np.mean(embedding_list, axis = 0)   
        return avg_embed.tolist()

    @staticmethod
    def cosine_simmilarity(db_embedding, current_embedding) -> bool:
        """Function to calculate cosine similarity between two embeddings

        Args:
            db_embedding (list): This embedding is extracted from the database
            current_embedding (list): This embedding is extracted from the current images

        Returns:
            int: simmilarity value
        """
        try:
            return np.dot(db_embedding, current_embedding) / (np.linalg.norm(db_embedding) * np.linalg.norm(current_embedding))
        except Exception as e:
            raise AppException(e, sys) from e

    def compareEmbedding(self, files: bytes) -> bool:
        """_summary_

        Args:
            db_embedding (list): _description_
            current_embedding (list): _description_

        Returns:
            bool: _description_
        """
        try:
            if self.user:
                # Validate user embedding
                if self.validate() == False:
                    return False

                # Generate embedding list
                embedding_list = UserLoginEmbeddingValidation.generateEmbeddingList(files)

                # Calculate average embedding
                avg_embedding_list = UserLoginEmbeddingValidation.averageEmbedding(embedding_list)
                
                # Get embedding from database
                db_embedding = self.user['user_embed']
                # Calculate cosine similarity
                simmilarity = UserLoginEmbeddingValidation.cosine_simmilarity(db_embedding, avg_embedding_list)
                if simmilarity >= SIMILARITY_THRESHOLD:
                    return True
                else:
                    return False
            return False
        except Exception as e:
            raise AppException(e, sys) from e

    
    def get_user_embeeding_object(self, uuid_:str) -> Embedding:
        """_summary_

        Args:
            user_embedding (dict): _description_

        Returns:
            Embedding: _description_
        """
        try:

            user_embedding = self.user_embedding_data.get_user_embedding(uuid_)
            return user_embedding
        except Exception as e:
            raise AppException(e, sys) from e

class UserRegisterEmbeddingValidation:
    def __init__(self, uuid_:str) -> None:
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()

    def saveEmbedding(self, files: bytes):
        """_summary_

        Args:
            user_embedding (dict): _description_

        Returns:
            Embedding: _description_
        """
        try:
            embedding_list = UserLoginEmbeddingValidation.generateEmbeddingList(files)
            avg_embedding_list = UserLoginEmbeddingValidation.averageEmbedding(embedding_list)
            self.user_embedding_data.save_user_embedding(self.uuid_, avg_embedding_list)
        except Exception as e:
            raise AppException(e, sys) from e
    
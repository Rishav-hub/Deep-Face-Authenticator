from face_auth.utils.util import CommonUtils

MONGODB_URL_KEY = CommonUtils().get_environment_variable("MONGODB_URL_KEY")
DATABASE_NAME = CommonUtils().get_environment_variable("DATABASE_NAME")
USER_COLLECTION_NAME = CommonUtils().get_environment_variable("USER_COLLECTION_NAME")
EMBEDDING_COLLECTION_NAME = CommonUtils().get_environment_variable(
    "EMBEDDING_COLLECTION_NAME"
)

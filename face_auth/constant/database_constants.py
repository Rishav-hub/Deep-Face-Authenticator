import os
from face_auth.utils.util import CommonUtils


ATLAS_CLUSTER_USERNAME= CommonUtils().get_environment_variable('ATLAS_CLUSTER_USERNAME')
ATLAS_CLUSTER_PASSWORD= CommonUtils().get_environment_variable('ATLAS_CLUSTER_PASSWORD')
DATABASE_NAME = CommonUtils().get_environment_variable('DATABASE_NAME')
USER_COLLECTION_NAME= CommonUtils().get_environment_variable('USER_COLLECTION_NAME')
EMBEDDING_COLLECTION_NAME= CommonUtils().get_environment_variable('EMBEDDING_COLLECTION_NAME')



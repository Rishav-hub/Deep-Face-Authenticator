# Face-Authenticator

### MongoDB keys
1. ID -: riishav@ineuron.ai
2. Ps -: test@123

## Run using Docker

```
docker build -t face_auth_dev_env --build-arg SECRET_KEY=KlgH6AzYDeZeGwD288to79I3vTHT8wp7 --build-arg ALGORITHM=HS256 --build-arg ATLAS_CLUSTER_USERNAME="rishav" --build-arg ATLAS_CLUSTER_PASSWORD="test123" --build-arg DATABASE_NAME="UserDatabase" --build-arg USER_COLLECTION_NAME="User" --build-arg EMBEDDING_COLLECTION_NAME="Embedding" . 
```



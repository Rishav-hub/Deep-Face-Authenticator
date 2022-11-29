![alt text](https://github.com/Rishav-hub/face_auth_dev/blob/b440f8d95722e3c26a917011a3f89c7aed7b711a/docs/68747470733a2f2f696e6575726f6e2e61692f696d616765732f696e6575726f6e2d6c6f676f2e706e67.png?raw=true)

# Face Authentication System

This is a modern Face Authentication System which includes state-of-art algorithms to detect face and generate face embedding. This system contains endpoints which can be integrated to any device depending on the requirements. 

## Project Archietecture
<img width="844" alt="image" src="https://user-images.githubusercontent.com/57321948/195135349-9888d9ea-af5d-4ee2-8aa4-1e57342add05.png">

## Run the Application
Before we run the project, make sure that you are having MongoDB in your local system, with Compass since we are using MongoDB for data storage. You also need Azure account to access the service like ACS and App services.

### Step 1-: Clone the Repository
```
git clone https://github.com/Rishav-hub/face_auth_dev.git
```

### Step 2-: Creat conda environment
```
conda create -p ./env python=3.8.13 -y
```

### Step 3-: Activate Conda environment
```
conda activate face_auth
```

### Step 4-: Install requirements
```
pip install -r requirements.txt
```

### Step 5-: Export the environment variable
```
export SECRET_KEY=<SECRET_KEY>

export ALGORITHM=<ALGORITHM>

export MONGODB_URL_KEY=<MONGODB_URL_KEY>

export DATABASE_NAME=<DATABASE_NAME>

export USER_COLLECTION_NAME=<USER_COLLECTION_NAME>

export EMBEDDING_COLLECTION_NAME=<EMBEDDING_COLLECTION_NAME>
```

### Step 6-: Run the application server
```
python app.py
```

## Run Locally

### Build the Docker Image
```
docker build -t face_auth --build-arg SECRET_KEY=<SECRET_KEY> --build-arg ALGORITHM=<ALGORITHM> --build-arg MONGODB_URL_KEY=<MONGODB_URL_KEY> --build-arg DATABASE_NAME=<DATABASE_NAME> --build-arg USER_COLLECTION_NAME=<USER_COLLECTION_NAME> --build-arg EMBEDDING_COLLECTION_NAME=<EMBEDDING_COLLECTION_NAME> . 
```

### Run the Docker Image

```
docker run -d -p 8000:8000 <IMAGEID OR IMAGENAME>
```
## Deployment to Azure

### Services used
- Azure container Registry (ACR) for Docker image of project is stored
- Azure App Services for deploying the application
- GitHub Actions for CI/CD

#### Please refer this [documentation](https://github.com/Rishav-hub/face_auth_dev/blob/main/docs/setup.md) for deployment to Azure.

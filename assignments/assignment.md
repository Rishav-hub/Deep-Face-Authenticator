# Assignment for Deep Authenticator

![alt text](https://github.com/Rishav-hub/face_auth_dev/blob/b440f8d95722e3c26a917011a3f89c7aed7b711a/docs/68747470733a2f2f696e6575726f6e2e61692f696d616765732f696e6575726f6e2d6c6f676f2e706e67.png?raw=true)


## Task 1.
The project which you have built, you need to modify the architecture of the project.

For example -:
1. You can use @dataclass for configuration management.
2. The User detail validation can be improved by adding more checks on the details entered by the user.

## Task 2.

Implement using different frameworks. Here we have used DeepFace package for face detection and embedding generation which used Tensorflow as framework.

1. Try using Pytorch. Refer this [facenet-pytorch](https://github.com/timesler/facenet-pytorch).

Create a proper document with explanation.

## Task 3.

Try to optimize the some components

Example -: 
1. We are pushing the embedding to MongoDB. Here we are pushing ndarrays to the database but you can convert it to bytes and then push it to Database.
2. Try using RDBMS databases on cloud like AWS RDS. Observe which method is fast NoSQL VS SQL.

## Task 4.

Here we have deployed using Azure Container regsitry and App Services.

1. Try using Azure Virtual Machines.
2. For CICD you have to use CircleCI.

## Task 5.

Here the Docker image size is more than 3GB.

1. Try reducing the docker image size and bring it below 2.5 GB.
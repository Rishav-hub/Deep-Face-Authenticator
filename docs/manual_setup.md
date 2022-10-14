![alt text](https://github.com/Rishav-hub/face_auth_dev/blob/b440f8d95722e3c26a917011a3f89c7aed7b711a/docs/68747470733a2f2f696e6575726f6e2e61692f696d616765732f696e6575726f6e2d6c6f676f2e706e67.png?raw=true)

# Face Authentication System Infrastructure Setup

## Azure Cloud Setup

First we need to have an Azure account with credit card attached to i, else we will not be abler to Azure cloud resources. Once that is done login to your Azure Account, with your credentials. Once you have successfully logged in to Azure Portal

## Installation of Azure CLI

### Install Azure CLI in Windows System

To install azure cli in windows system, open the terminal in adminstrator mode and execute the following command

```bash
$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindows -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; rm .\AzureCLI.msi
```

After sometime the installation should be successfull, then you can check the status of azure cli

### Install Azure CLI in Linux System

To install azure cli in linux system, execute the following commands

```bash
curl -L https://aka.ms/InstallAzureCli | bash
```

### Install Azure CLI in MacOS system

To install azure lic in MacOS system, execute the following commands

```bash
brew update
```

```bash
brew install azure-cli
```

### Check Azure CLI status

To check whether azure cli is working or not, execute the following commands

```bash
az version
```

On successfull, execution of the command, you will be able to the azure cli version which confirms that azure cli is working fine.

## Setup Azure Subscriptions

Before we use or access the azure resources, we need to create a subscription. On successfull login we will be able to see the azure portal from which we can create subscriptions. Navigate to subscriptions, and the click on that you will be navigated to subscriptions page, where you will see list of all subscriptions, by default there will no subscriptions with your account. 

In the subscriptions page you will see a add button, and then select your subscription type as pay as you go, click on select offer. On clicking that you will redirected to login page, and accept to the agreement and click on next and then verify your identity via phone, any method of verifaction is fine like text message or call option. 

Once the verifaction is done, add your credit card details and once the credit card details are added click on next and you will be asked for your address provide that and click on sign up. Wait for some time, you will be redirected to azure portal, and in the subscriptions category you will see that there is new subscription created. 

Note that everything you create in azure will be tagged to this subscription itself.

## Resource Group Creation

Now that the subscriptions are created, we have to resource group where our resources will be created. To create the resource group go to the search bar and type resource groups and press enter, you will be navigated to resource groups page, by default no resource groups will be there, click on create resource group and you will be navigated to create resource group page, in there type the resource group name as "{your_project_name}rg", and then click on review + create button, once the validation is done, click on create and the resource group will be created.

## Creating Azure Container Registry for storing Docker images

To create azure container registry, we need to have existing resource group created. Once the resource group is created we can proceed to create the resource in the resource group. In the resource group page, there will be resource group named "{your_project_name}rg", click on that and then you will be navigated to the resource group page, by default, there are no resources created in resource group.

To create a container registry, click on create button and you will be redirected to azure marketplace there in the search bar type "container registry" and create first option where container registry is shown, click create button and you will be redirected to create container registry page, in that give the registry name as "{your_project_name}acr", leave other options as default and click on review and create button and after the validation is completed, click on create button and container registry resource will start getting created. Once the container registry is created, click on the go to resource and you will redirected to container registry page. During deployment we need the REGISTRY_USERNAME and REGISTRY_PASSWORD, for authentication purposes. 

In order to get these credentials, in the container registry page, you will see that in the settings tab column there is a option of access keys, for getting the REGISTRY_PASSWORD and REGISTRY_USERNAME, enable the admin user option and you will be able to username, password and password2. For REGISTRY_USERNAME use the username, and REGISTRY_PASSWORD use any of password and password2. 

Store these credentials in github secrets. If we see the deployment workflow, there is secret name AZURE_LOGIN_SERVER which is login server present in the access key page. One more secret is REPO_NAME use {your_project_name}. 

## Creating Azure Web App Service

To create azure web app service , we need to have existing resource group created. Once the resource group is created we can proceed to create the resource in the resource group. In the resource group page, there will be resource group named "{your_project_name}rg", click on that and then you will be navigated to the resource group page. 

Before creating the web app service, make sure that your container image is pushed to azure container registry, then only your application image will be deployed properly. Once that is done click on create button and in the search bar, type "container web app", and then click on the first option and then click on create. 

Now you will be redirected to create web app page, select the web app name as {your_project_name}, in the publish section select docker container, and leave everything to default. Now click on "next -> docker" button, and in that select the image source as "Azure Container Registry" and in the registry, select the previously created registry name.

Now click on "review and create" button and then click on create button, to create and deploy the container image in azure web app. Wait for the creation of resources to be completed. Once the creation of resources is done, click on the go to resource and you will redirected to web app page, where you will find the url of the container image.

Before, we open the url we need to add some additional settings to the resource like WEBSITES_PORT and WEBSITES_CONTAINER_START_TIME_LIMIT. To add these additional settings, we need to click on the configuration of settings column, once you click on that, you will directed to configuration page under which you find the application settings. 

Now click on "new application setting" button and give the name as "WEBSITES_CONTAINER_START_TIME_LIMIT" and the value as 20 if the image size is small (around 1GB or so) and value as 60 is image size is big (around 3GB). In the similar way add WEBSITES_PORT as name with value to be your container port number. Once this is done, click on save and then click continue. 

After a few seconds, the application settings will be reflected. Now click on overview tab, and copy the url of webapp present under "URL". After sometime, you can see that web app is running and application is accessible by the internet using the given url.

## Creating Azure Credentials for automating the deployments via GitHub Actions

In order to perform automatic deployments to Azure Web App via GitHub actions, we need to create azure credentials, before we proceed to create azure credentials make sure that azure cli is installed in your system. Once that is done, execute the following command, to create a role in Azure which will give credentials to deploy to azure web app via github actions. 

NOTE -: Execute this command in command prompt or powershell terminal.

```bash
az ad sp create-for-rbac --name "<your_app_name>_login_role" --role contributor --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group-name> --sdk-auth
```

Fill in the neccessary details, in the command mentioned above, like "your_app_name", "subscription-id" and "resource-group-name". On successfull execution of the commands, you will get json output, copy the josn output and paste it in the github secrets with AZURE_CREDENTIALS as the name.

Once that is done, you will be able to perform automatic deployments to azure web app from github actions whenever there is code change to github.

## Destroying all the Azure Resources created

Once the project setup is done, and you have tested your application in the cloud. It is time to destroy the resources which we have created in Azure so that we do not incur any extra charges, to delete all the resources at a time, click on the resource group section and then click your resource group name, and once it is done you will directed to resource group page, there you will find a "Delete resource group" button, click on that, and type the resource group name in the space provided and click on delete. After sometime the resource group will be deleted and along with that all the created resources.

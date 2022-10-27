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

## Install Terraform 

### Install Terraform in Linux System

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common curl
```

```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -

```

```bash
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
```

```bash
sudo apt-get update && sudo apt-get install terraform
```

### Install Terraform in Windows System

To install terraform in windows, first we have to install choco package manager, first open the powershell or command prompt with administrator access and then execute the following commands

```bash
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

To check choco installation is working or not, execute the following

```bash
choco --version
```

Once the choco installation is working fine, we can go forward with the installation of terraform

```bash
choco install terraform
```

### Check for terraform installation

To check whether the terraform installation is working fine or not. Execute the following commands

```bash
terraform --version
```

### Infrastructure Setup

Once the installation of terraform and azure cli are done we can start executing the terraform commands to provision the infrastructure in Azure cloud. Before we execute the terraform commands we need to login to azure account using azure cli.

```bash
az login 
```

On successfull execution of the command, we will a tab opening the browser asking you to approve the login, after the approval is done we have successfully logged in to azure via cli.

Before we provision the infrastructure using terraform, we need to configure the backend which is Azure Blob Storage backend. In order to make things simplier we have created bash scripts in order to create and delete initial setup of terraform azure backend. The scripts can be found the scripts folder of the repository

Before executing the scripts, we need to replace <your_app_name> to a any unique name, since the resource groups in azure have to globally unique. Once the change is done, we can execute the bash scripts, to create the initial terraform backend setup in azure. 

```bash
bash scripts/create_initial_setup.sh
```

On successfull exectution of the commands, we will see that there will be resource group created in azure. In that resource group, there will be storage account which would have a container present it. Once you are able to see this it means that we have successfully setup the terraform backend in azure, we can provision the infrastructure using terraform scripts.

Before running the terraform commands , we need to replace <your_app_name> in module.tf file with the same name as mentioned in the scripts/create_initial_setup.sh file, the same goes for scripts/delete_initial_setup.sh this is will deleting the infrastructure. Once the required changes are done.

```bash
terraform -chdir=infrastructure/ validate
```

This command validates whether the terraform modules are syntactically correct or not. If the terraform modules are syntactically correct, you will get response as "Success! The configuration is valid". Once the validation of the modules are done, we can initialize them using the following command

```bash
terraform -chdir=infrastructure/ init
```

Now successfull execution of the commands, we will see that terraform modules are initialized with azure blob storage backend, and if we go to backend container which was created by the initial setup script, there will be blob (object) been created. This means that the terraform backend is successfully initialized.

```bash
terraform -chdir=infrastructure/ plan
```

This command plans the terraform modules, it is like trying to get the output of the terraform modules without actually creating it. On successfully exectution of command, you will be able to planned infrastructure, like what resources will be created or destroyed.

```bash
terraform -chdir=infrastructure/ apply --auto-approve
```

This commands applies the terraform modules and creates or make any changes to the infrastructure as per the terraform module changes. After some time the terraform modules will be applied and required resources get created the Azure Cloud.

## Creating Azure Credentials for automating the infrastructure provisioning using GitHub Actions

In order to perform automatic infrastucture provisioning in Azure Cloud using GitHub Actions we need to create azure credentials, before we proceed to create azure credentials make sure that make sure that azure cli is installed in your system. Once that is done, execute the following command, to create a role in Azure which will give credentials to automate infrastructure provisioning using github actions

NOTE -: Execute this command in command prompt or powershell terminal.

```bash
az ad sp create-for-rbac --name "<your_app_name>_terraform_role" --role contributor --scopes /subscriptions/<subscription-id> --sdk-auth
```

On successfull execution of the command, there will be json output, we need to note down some of the values and updated them in GitHub secrets. Some of the values which are to be noted are

AZURE_AD_CLIENT_ID - json value of clientId

AZURE_AD_CLIENT_SECRET - json value of clientSecret

AZURE_SUBSCRIPTION_ID - subscription-id

AZURE_AD_TENANT_ID - json value of tenantId

Once these values are noted, updated these in Github secrets with the same name. Once that is done, terraform infrastructure provisioning is automated by using GitHub actions and it will be triggered when there are changes in the infrastructure folder of the repository.

## Creating Azure Credentials for automating the infrastructure provisioning using GitHub Actions

In order to perform automatic infrastucture provisioning in Azure Cloud using GitHub Actions we need to create azure credentials, before we proceed to create azure credentials make sure that make sure that azure cli is installed in your system. Once that is done, execute the following command, to create a role in Azure which will give credentials to automate infrastructure provisioning using github actions

NOTE -: Execute this command in command prompt or powershell terminal.

```bash
az ad sp create-for-rbac --name "<your_app_name>_terraform_role" --role contributor --scopes /subscriptions/<subscription-id> --sdk-auth
```

On successfull execution of the command, there will be json output, we need to note down some of the values and updated them in GitHub secrets. Some of the values which are to be noted are

AZURE_AD_CLIENT_ID - json value of clientId

AZURE_AD_CLIENT_SECRET - json value of clientSecret

AZURE_SUBSCRIPTION_ID - subscription-id

AZURE_AD_TENANT_ID - json value of tenantId

Once these values are noted, updated these in Github secrets with the same name. Once that is done, terraform infrastructure provisioning is automated by using GitHub actions and it will be triggered when there are changes in the infrastructure folder of the repository.

## Destroying all the Azure Resources created

Once the project setup is done, and you have tested your application in the cloud. It is time to destroy the resources which we have created in Azure so that we do not incur any extra charges, to delete all the resources. Execute the following commands

```bash
terraform -chdir=infrastructure/ destroy --auto-approve
```

```bash
bash scripts/delete_initial_setup.sh
```

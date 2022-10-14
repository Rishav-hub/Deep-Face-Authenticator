#!bin/bash

az group create -n <your_app_name>tfstate -l eastus2
 
az storage account create -n <your_app_name>tfstate -g <your_app_name>tfstate -l eastus2 --sku "Standard_LRS"
 
az storage container create -n tfstate --account-name <your_app_name>tfstate

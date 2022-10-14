#!bin/bash

az group create -n faceapptfstate -l eastus2
 
az storage account create -n faceapptfstate -g faceapptfstate -l eastus2 --sku "Standard_LRS"
 
az storage container create -n tfstate --account-name faceapptfstate

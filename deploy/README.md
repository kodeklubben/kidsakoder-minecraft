kidsakoder-minecraft
====================

## Architecture
#### Cloud providers
* [Microsoft Azure](https://azure.microsoft.com/en-us/)
* ~~[Amazon Web Services (AWS)](https://aws.amazon.com/)~~

#### DNS providers
* [DNSimple](https://dnsimple.com/)


## Requirements
#### Terraform
In order to deploy and orchestrate the cloud infrastructure (storage, network, security, instances and  etc.), a tool called [Terraform](https://terraform.io) is used. 
Terraform is a multi-platform tool which supports writing infrastructure as code for multiple different cloud providers such as Azure, AWS. 
See the [Terraform documentation](https://www.terraform.io/docs/index.html) for more infomation on how it works.

##### Installation
Follow the guide on how to [install Terraform](https://www.terraform.io/intro/getting-started/install.html) and verify it by executing `terraform` in a terminal. 

###### Windows
For Windows, the terminal [Cmder](http://cmder.net) is highly recommended as it supports color output, ssh, git and other things.

---

#### Azure 
##### Authentication
In order to authenticate with Azure, Terraform needs a **publish settings** file from Azure which can be found [here](https://manage.windowsazure.com/publishsettings). 
Rename the file to `secret.publishsettings` and place it under `provision/`.

##### SSH Settings
As of right now, only authentication with username and password via SSH works.
Use the [terraform.tfvars.example](terraform/terraform.tfvars.example) as a template and fill in the SSH settings in `terraform/terraform.tfvars`.  

---

#### DNSimple 
[DNSimple](https://dnsimple.com) is used to manage the domain and records for this project.

##### Authentication 
In order to create and edit DNS records, Terraform needs the **email** and an **API token** of a DNSimple account.
The **API token** can be found on the [user page](https://dnsimple.com/user) on DNSimple.
Use the [terraform.tfvars.example](terraform/terraform.tfvars.example) as a template and fill in the email and API token in `terraform/terraform.tfvars`.  

_Please note that **Single-domain tokens** do not work as of writing._


## How to deploy
### Deploy to Azure
```
# Make sure you are in the provision directory
cd terraform/

# Generate an execution plan of what Terraform plans to deploy
terraform plan 

# Build the infrastructure
terraform apply 
```

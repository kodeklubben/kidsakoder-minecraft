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

---

#### Azure 
##### Authentication
In order to authenticate with Azure, Terraform needs a **publish settings** file from Azure which can be found [here](https://manage.windowsazure.com/publishsettings).

Name the file `secret.publishsettings` and place it [provision/secret.publishsettings](provision/secret.publishsettings).
##### SSH Settings
Use the [provision/secrets.tfvars.example](provision/secret.tfvars.example) as a template and fill in the SSH settings in [provision/secrets.tfvars](provision/secret.tfvars)

---

#### DNSimple 
[DNSimple](https://dnsimple.com) is used to manage the domain and records for this project.
##### Authentication
For DNS records hosted on DNSimple, Terraform needs the **email** and an **API token** of a DNSimple account. Note: Single-domain tokens do not work as writing.

The **API token** can be found on the [user page](https://dnsimple.com/user) on DNSimple.

Use the [provision/secrets.tfvars.example](provision/secret.tfvars.example) as a template and fill in the authentication information in [provision/secrets.tfvars](provision/secret.tfvars)


## How to deploy
### Deploy to Azure
```
# Make sure you are in the provision directory
cd provision/

# Generate an execution plan of what Terraform plans to deploy
terraform plan -var-file=secret.tfvars

# Build the infrastructure
terraform apply -var-file=secret.tfvars
```

kidsakoder-minecraft
====================

## Deployment

### Requirements
#### Terraform
[Terraform](https://terraform.io)

#### Platforms
##### Azure 
###### Authentication
In order to authenticate with Azure, Terraform needs a **publish settings** file from Azure which can be found [here](https://manage.windowsazure.com/publishsettings).

Name the file `secret.publishsettings` and place it [bootstrap/secret.publishsettings](bootstrap/secret.publishsettings).

##### DNSimple 
###### Authentication
For DNS records hosted on DNSimple, Terraform needs the **email** and an **API token** of a DNSimple account. Note: Single-domain tokens do not work as writing.

The **API token** can be found on the [user page](https://dnsimple.com/user) on DNSimple.

Fill in the information in [bootstrap/secrets.tfvars](bootstrap/secret.tfvars).

#### How to deploy

```
# Make sure you are in the bootstrap directory
cd bootstrap/

# Generate an execution plan of what Terraform plans to deploy
terraform plan -var-file=secret.tfvars

# Build the infrastructure
terraform apply -var-file=secret.tfvars
```

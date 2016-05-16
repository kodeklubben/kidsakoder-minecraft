kidsakoder-minecraft
====================
[![Build Status](https://travis-ci.org/szeestraten/kidsakoder-minecraft.svg?branch=master)](https://travis-ci.org/szeestraten/kidsakoder-minecraft)

## Project information
### Tools used
#### Configuration management
[Salt](http://saltstack.com/community/) from [SaltStack](http://saltstack.com/) is the configuration management tool used in this project.
See the [Salt Docs](https://docs.saltstack.com/en/latest/) for more documentation.

#### Development environment
In order to ease the development and testing of this project, a tool called [Vagrant](https://www.vagrantup.com/) is used.
Vagrant allows for easily creating defined local development environments with virtual machines using [Virtualbox](https://www.virtualbox.org/) or other providers.
The aim is to define an environment that looks like the production environment (such as the cloud) that is the same for everyone so developers can quickly test changes without impacting the production environment.

#### Deployment
In order to deploy and orchestrate the cloud infrastructure (storage, network, security, instances and  etc.), a tool called [Terraform](https://terraform.io) is used.
Terraform is a multi-platform tool which supports writing infrastructure as code for multiple different cloud providers such as Azure, AWS.
See the [Terraform docs](https://www.terraform.io/docs/index.html) for more information on how it works.

## Requirements
### Tools
#### Python
This project uses **Python 2.7** and **pip** for installing packages.

Install **Python 2.7.x** (pip should be included) from [here](https://www.python.org/downloads/) and make sure they are both in your path.

You can follow [this guide](http://www.anthonydebarros.com/2011/10/15/setting-up-python-in-windows-7/) for how to add Python and pip to the path in Windows.

You can verify and check which versions are installed by running the commands below in your terminal.

```
# Check Python version
python --version

# Check pip version
pip --version
```

#### Vagrant
Install Vagrant and Virtualbox from the links below:
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

You can verify that Vagrant is installed by running the following in your terminal.
```
vagrant --version
```

#### Terraform
Follow the guide on how to [install Terraform](https://www.terraform.io/intro/getting-started/install.html), and make sure that Terraform has been added to your path.

You can verify that Terraform is installed and added to your path by running the following in your terminal.
```
terraform --version
```

If you are using Windows, the terminal [Cmder](http://cmder.net) is highly recommended as it supports color output, SSH, git out of the box.


### External resources
#### Azure
> **WARNING:** If you're not using a free trial account, then you will be charged for using Azure resources.

In order to deploy this project, you need to have an active Azure subscription.


TODO: Add more details on free trial


##### Step 1: Download the Azure publish settings file
> **WARNING:** The Azure publish settings file contains credentials to administer your Azure subscription and services. Please make sure you store it safely.

In order to use Terraform with Azure, Terraform needs a credential file called **publish settings** file from Azure which can be found [here](https://manage.windowsazure.com/publishsettings).

Rename the file to `secret.publishsettings` and place it in the `terraform/` directory.

##### Step 2: Create Azure certificates for Salt Cloud
> **WARNING:** The Azure certificates contains credentials to administer your Azure subscription and services.
Please make sure you store it safely.
If either certificates are compromised, you'll need to revoke the management certificate in the Azure management portal.

In order for Salt to create machines in Azure, two are certificates are needed:

A `.cer` file, which is uploaded to Azure via the "Upload a Management Certificate" action of the "Management Certificates" tab within the "Settings" section of the old [management portal](https://manage.windowsazure.com).

A `.pem` file called `kidsakoder.pem` which should be placed in [saltstack/etc/](saltstack/etc/).
The `.pem` file will be distributed to the Salt Master so it can create and destroy VMs.


###### How to generate certificates
```
# Generate the .pem file
openssl req -x509 -nodes -days 1068 -newkey rsa:4096 -keyout kidsakoder.pem -out kidsakoder.pem

# Generate .cer certificate from .pem file
openssl x509 -inform pem -in kidsakoder.pem -outform der -out kidsakoder.cer
```

*Windows:* If you are using Windows, use [Git Shell in Github Desktop](https://desktop.github.com/), [Git for Windows](https://git-for-windows.github.io/), [Cmder](http://cmder.net), or simply use one of the Linux VMs created by Vagrant.

*Taken from [Salt Cloud documentation](https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration).*

##### Step 3: Create SSH keys for Azure
> **WARNING:** The SSH keys

TODO: Add info about SSH


###### How to generate SSH keys
```
# Create a new ssh key type RSA, 4096 bits, with the filename kidsakoder, using the provided email as a label
ssh-keygen -t rsa -b 4096 -f kidsakoder -C "your_email@example.com"
```
*Windows:* If you are using Windows, use [Git Shell in Github Desktop](https://desktop.github.com/), [Git for Windows](https://git-for-windows.github.io/), [Cmder](http://cmder.net), or simply use one of the Linux VMs created by Vagrant.


#### DNSimple
[DNSimple](https://dnsimple.com) is used to manage the domain and records for this project.

Right now it is only to create a domain record for the master server.

In order to create and edit DNS records, Terraform needs the **email** and an **API token** of a DNSimple account.
The **API token** can be found on the [user page](https://dnsimple.com/user) on DNSimple.
Use the [terraform.tfvars.example](terraform/terraform.tfvars.example) as a template and fill in the email and API token in `terraform/terraform.tfvars`.  

_Please note that **Single-domain tokens** do not work as of writing._



## How to develop
### Just developing on the Flask web app?
#### Requirements
First, make sure you have `Python` and `pip` installed.
To install Flask and any other requirements, run the following:
```
pip install -r requirements.txt
```
#### Running Flask locally
To run Flask locally on `http://localhost:5000`, you need to do the following:

Setup the app by running the following command in the project folder:
```
python setup_app.py
```
This will generate a secret key, create a secret config file and initialize the database.

Then start the server by running:
```
python runserver.py
```

### Deploying to local virtual machines?
See [Development environment](#Development-environment) for why we are using Vagrant and the [Vagrant Docs](https://www.vagrantup.com/docs/) for more documentation.

#### Development environment
The Vagrant environment is defined in [Vagrantfile](Vagrantfile).
It defines 2 different virtual machines which are listed below.
The aim is to replicate the different virtual machines that are deployed in production.
The virtual machines are configured and installed using Salt based on the Salt States and Pillars in [saltstack/](saltstack/) (see [Configuration management](#Configuration-management) for more details).

_Please note that the `mc` server require that the `master` server is up in order for Salt to get the configuration files from the master._

| VM Name | Role                     | Configuration Mgmt.        | IP              | Port-Forwarding                   | VM Memory |
|---------|--------------------------|----------------------------|-----------------|-----------------------------------|-----------|
| master  | Salt Master & Web Server | Master                     | 192.168.100.100 | Guest: 80, 5000, Host: 8080, 5000 | 1024 MB   |
| mc      | Minecraft Server         | Minion (depends on Master) | 192.168.100.101 | Guest: 25565, Host: 25565         | 1024 MB   |


#### How to use Vagrant
```
### General commands
# List the status of the virtual machines in this environment
vagrant status

# Create/start the virtual machines in the environment
vagrant up

# Connect to virtual machine via SSH
vagrant ssh <machine name>

# Destroy the virtual machines in the environment
vagrant destroy

# Shutdown the virtual machines environment to save resources
vagrant halt

# Restart a virtual machine
vagrant reload <machine name>

### Scenario: Test changes in Minecraft server configuration
# Create/start Master and Minecraft servers
vagrant up master mc

# If Minecraft server already create, run provisioning steps again
vagrant provision mc
```


## Deployment
### Architecture
| Service        | Name                      | Supported |
|----------------|---------------------------|-----------|
| Cloud platform | [Microsoft Azure](https://azure.microsoft.com/en-us/)           | Yes       |
| Cloud platform | [Amazon Web Services (AWS)](https://aws.amazon.com/) | Not yet   |
| DNS provider   | [DNSimple](https://dnsimple.com/)                  | Yes       |


### Requirements
#### Terraform
First make sure `Terraform` is installed:

Terraform uses SSH to provision the initial virtual machines when deploying.
As of right now, it only supports authentication with username and password.
Use the [terraform.tfvars.example](terraform/terraform.tfvars.example) as a template and fill in the SSH settings in `terraform/terraform.tfvars`.  

#### Azure

### How to deploy with Terraform
Make sure you are in the [terraform](terraform/) directory when you are using Terraform to deploy.

#### Initial deployment
```
# Get the Terraform modules used in this directory
# NOTE: Only needed when running for the first time or changes have been made to the modules
terraform get

# Generate an execution plan of what Terraform plans to deploy
terraform plan

# Build the infrastructure
terraform apply
```

#### Changing the infrastructure
```
# See how the changes will impact the infrastructure
terraform plan

# Apply any changes
terraform apply
```

##### Redeploying a resource in a module
If one needs to redeploy a resource (such as a VM), one can use the `taint` command in Terraform.
If a resource has been tainted, Terraform will try to destroy and recreate it the next time you run `apply`.
Again, before applying any changes, it is smart to see what Terraform is planning to do by running `play` first.
Should you taint the wrong resource, you can easily revert it by using the `untaint` command.

###### Taint command format
```
# In order to redeploy a resource, you can taint it.
terraform taint -module=<module-name> <resource_type>.<resource_name>

# In case a resource has been tainted by accident, you can just untaint it.
terraform untaint -module=<module-name> <resource_type>.<resource_name>
```

###### Example scenario: redeploying the Salt master using taint
```
# Here we taint the Salt master which is an Azure instance in the master module.
terraform taint -module=master azure_instance.master

# See how the changes will impact the infrastructure
terraform plan

# Apply the changes to the infrastructure
terraform apply
```

---

## Contributing
### Project coding conventions
#### Branch naming
```
feat_       Features
bugfix_     Bug fixes
exp_        Experimental
(If using / in branch name, waffle will interpret as cross repo reference and not move issue automatically)
```

#### Pull requests
When creating pull requests, use the keyword `closes` to group with issue in waffle.
```
feat_add-flask closes #33
```

##### Examples
```
feat_add-flask-#33          A new feature branch for adding Flask in issue #33
bugfix_typo-in-header-#21   A bug fix branch to fix a typo in issue #21
exp_testing-mysql           An experimental branch for testing my-sql
```

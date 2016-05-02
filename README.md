kidsakoder-minecraft
====================

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

Make a copy of (do not rename) `secret_config.py.template` in `flask_app/config` and name it `secret_config.py`. Then you can fill in your super secret config settings.

Setup the app by running the following command in the project folder:
```
python setup_app.py
```
This will generate a secret key and initialize the database.
Then start the server by running:
```
python runserver.py
```

### Deploying to local virtual machines?
#### Requirements
In order to create the development environment using local virtual machines, [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://virtualbox.org) need to be installed.
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

See [Development environment](#Development-environment) for why we are using Vagrant and the [Vagrant Docs](https://www.vagrantup.com/docs/) for more documentation.

#### Development environment
The Vagrant environment is defined in [Vagrantfile](Vagrantfile).
It defines 3 different virtual machines which are listed below.
The aim is to replicate the different virtual machines that are deployed in production.
The virtual machines are configured and installed using Salt based on the Salt States and Pillars in [saltstack/](saltstack/) (see [Configuration management](#Configuration-management) for more details).

_Please note that the `web` and `mc` servers require that the `master` server is up in order for Salt to get the configuration files from the master._

| VM Name | Role             | Configuration Mgmt.        | IP              | Port-Forwarding                   | VM Memory |
|---------|------------------|----------------------------|-----------------|-----------------------------------|-----------|
| master  | Salt Master      | Master                     | 192.168.100.100 | None                              | 512 MB    |
| web     | Web Server       | Minion (depends on Master) | 192.168.100.101 | Guest: 80, 5000, Host: 8080, 5000 | 256 MB    |
| mc      | Minecraft Server | Minion (depends on Master) | 192.168.100.102 | Guest: 25565, Host: 25565         | 1024 MB   |

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
Follow the guide on how to [install Terraform](https://www.terraform.io/intro/getting-started/install.html) and verify it by executing `terraform` in a terminal. 
If you are using Windows, the terminal [Cmder](http://cmder.net) is highly recommended as it supports color output, ssh, git and other things.
See the [Terraform documentation](https://www.terraform.io/docs/index.html) for more infomation on how it works.
##### SSH Settings
Terraform uses SSH to provision the initial virtual machines when deploying.
As of right now, it only supports authentication with username and password.
Use the [terraform.tfvars.example](terraform/terraform.tfvars.example) as a template and fill in the SSH settings in `terraform/terraform.tfvars`.  

#### Azure 
##### Authentication
In order to authenticate with Azure, Terraform needs a **publish settings** file from Azure which can be found [here](https://manage.windowsazure.com/publishsettings). 
Rename the file to `secret.publishsettings` and place it in the `terraform/` directory.

##### Generating keys and certificates
In order for Salt to create machines in Azure, two are certificates are needed:

A `.cer` file, which is uploaded to Azure via the "Upload a Management Certificate" action of the "Management Certificates" tab within the "Settings" section of the old [management portal](https://manage.windowsazure.com).

A `.pem` file called `kidsakoder.pem` which should be placed in [saltstack/etc/](saltstack/etc/).

###### Steps to generate keys and certificates
```
# Generate the .pem file
openssl req -x509 -nodes -days 1068 -newkey rsa:4096 -keyout kidsakoder.pem -out kidsakoder.pem

# Generate .cer certificate from .pem file
openssl x509 -inform pem -in kidsakoder.pem -outform der -out kidsakoder.cer
```

#### DNSimple 
[DNSimple](https://dnsimple.com) is used to manage the domain and records for this project.

##### Authentication 
In order to create and edit DNS records, Terraform needs the **email** and an **API token** of a DNSimple account.
The **API token** can be found on the [user page](https://dnsimple.com/user) on DNSimple.
Use the [terraform.tfvars.example](terraform/terraform.tfvars.example) as a template and fill in the email and API token in `terraform/terraform.tfvars`.  

_Please note that **Single-domain tokens** do not work as of writing._


### How to deploy
Make sure you are in the [terraform](terraform/) directory when you are using Terraform to deploy.

#### Initial deployment
```
# Generate an execution plan of what Terraform plans to deploy
terraform plan 

# Build the infrastructure
terraform apply
```

#### Changing the infrastructure
```
# See how the changes will impact the infrastructure
terraform plan 

# If there is an resource that needs to be redeployed use the taint command
terraform taint azure_instance.webserver

# Apply the changes to the infrastructure
terraform apply
```

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

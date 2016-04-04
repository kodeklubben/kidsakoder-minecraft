kidsakoder-minecraft
====================

## Project information
### Tools
##### Configuration management
[Salt](http://saltstack.com/community/) from [SaltStack](http://saltstack.com/) is the configuration management tool used in this project.
See [Salt Docs](https://docs.saltstack.com/en/latest/) for more documentation.


## How to get started
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
This will generate a secret key and initialize the database.
Then start the server by running:
```
python runserver.py
```

### Deploying to local virtual machines?
In order to ease the development and testing of this project, a tool called [Vagrant](https://www.vagrantup.com/) is used.
Vagrant allows for easily creating defined local development environments with virtual machines using [Virtualbox](https://www.virtualbox.org/) or other providers. 
The aim is to define an environment that looks like the production environment (such as the cloud) that is the same for everyone so developers can quickly test changes without impacting the production environment.

#### Requirements
First, make sure you have [Vagrant](https://www.vagrantup.com/downloads.html) installed. 
It supports Windows, Mac OS X and Linux.
See [Vagrant Docs](https://www.vagrantup.com/docs/) for more documentation.

#### Development environment
The Vagrant environment is defined in [Vagrantfile](Vagrantfile).
It defines 3 different virtual machines which are listed below.
The aim is to replicate the different virtual machines that are deployed in production.
The virtual machines are configured and installed using Salt based on the Salt States and Pillars in [deploy/saltstack](deploy/saltstack) (see [Configuration management](#Configuration-management) for more details).

_Please note that the `web` and `minecraft` servers require that the `master` server is up in order for Salt to get the configuration files from the master._

| Virtual Machine | Role             | Configuration Mgmt. | Port-Forwarding       |
|-----------------|------------------|---------------------|-----------------------|
| master          | Salt Master      | Salt Master         | None                  |
| web             | Web Server       | Salt Minion         | Guest: 80, Host: 8080 |
| minecraft       | Minecraft Server | Salt Minion         | None                  |

#### Using Vagrant to create the local development environment
```
# Create all the virtual machines
vagrant up

# List the status of the virtual machines in this environment
vagrant status

# Destroy the environment
vagrant destroy

# Restart a virtual machine
vagrant reload <machine name>

# Create a virtual machine
vagrant up <machine name>

# Run provisioning again on a virtual machine
vagrant provision <machine name>
```

### Deploying to production?
See [README.md](deploy/README.md) in [deploy/](deploy/) for more details on how to deploy to production.


## Coding conventions
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

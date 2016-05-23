# Salt State for setting up Salt Cloud

# Install dependencies for Salt Cloud
# See https://docs.saltstack.com/en/latest/topics/cloud/azure.html#dependencies
apache-libcloud:
  pip.installed:
    - name: apache-libcloud
    - require:
      - pkg: python-pkgs

azure:
  pip.installed:
    - name: azure >= 0.10.2, < 1.0.0
    - require:
      - pkg: python-pkgs

salt-cloud:
  pkg.installed:
    - name: salt-cloud
    - require:
      - pip: apache-libcloud


# Pull down latest Salt bootstrap script for Salt Cloud due to issue #26699 in Salt
salt-cloud-bootstrap-script:
  cmd.wait:
    - name: salt-cloud -u
    - cwd: /
    - watch:
      - pkg: salt-cloud


# Create Salt user for external authentication with Flask app
# The users permissions are defined in saltstack/etc/master.conf
salt-cloud-user:
  user.present:
    - name: salt-cloud
    - password: $6$H_WomOt8$y2Judd2oYDl7QLvNO5O9QEPDL5/OLTdkRy7UwLRiWc24F3Uth6GxtaZscBnIVnpCflEytJB4fm1CqZTmdBDE9.
    - shell: /bin/bash


# Setup Azure management certificate
azure-certificate:
  file.managed:
    - name: /etc/salt/azure.pem
    - source: salt://cloud/files/azure.pem


# Create Salt Cloud provider configuration from data in Pillar
# See https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration
azure-provider:
  file.managed:
    - name: /etc/salt/cloud.providers.d/azure.conf
    - source: salt://cloud/cloud.providers.d/azure.conf
    - template: jinja

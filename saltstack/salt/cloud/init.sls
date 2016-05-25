# Salt State for setting up Salt Cloud

# Install dependencies for Salt Cloud
# See https://docs.saltstack.com/en/latest/topics/cloud/azure.html#dependencies
apache-libcloud:
  pip.installed:
    - name: apache-libcloud
    - require:
      - pkg: python-pkgs

azure-python-sdk:
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


# Setup Azure management certificate
azure-certificate:
  file.managed:
    - name: /etc/salt/azure.pem
    - source: salt://cloud/files/azure.pem


# Create Salt Cloud provider and profiles from data in Pillar
# See https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration
azure-provider:
  file.managed:
    - name: /etc/salt/cloud.providers.d/azure-providers.conf
    - source: salt://cloud/files/azure-providers.conf.j2
    - template: jinja

azure-profiles:
  file.managed:
    - name: /etc/salt/cloud.profiles.d/azure-profiles.conf
    - source: salt://cloud/files/azure-profiles.conf.j2
    - template: jinja


# Create Salt user for external authentication with Flask app
# The users permissions are defined in saltstack/etc/master.conf
salt-cloud-flask-user:
  user.present:
    - name: salt-cloud-flask
    - password: $6$g_U_4iC1$APZjc8rLjAtvef4t8BIKuzFOLH6oyEQbjpOe/IrLeRLyG..w0FdG49tdPnSMbSICOfoIo35d/1F0ltLeO4A/X0
    - shell: /usr/sbin/nologin

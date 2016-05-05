# Install dependencies for Salt Cloud
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


# Create Azure cloud configs
azure-provider:
  file.managed:
    - name: /etc/salt/cloud.providers.d/azure.conf
    - source: salt://cloud/cloud.providers.d/azure.conf
    - template: jinja

azure-profile:
  file.managed:
    - name: /etc/salt/cloud.profiles.d/azure.conf
    - source: salt://cloud/cloud.profiles.d/azure.conf
    - template: jinja


# Upload our Salt Cloud Azure python module
azure-python-module:
  file.managed:
    - name: /etc/salt/azure.py
    - source: salt://cloud/azure.py

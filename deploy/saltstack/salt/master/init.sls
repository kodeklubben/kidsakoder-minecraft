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


# Create cloud provider and profile configs
/etc/salt/cloud.providers.d/azure.conf:
  file.managed:
    - source: salt://cloud/cloud.providers.d/azure.conf
    - template: jinja

/etc/salt/cloud.providers.d/azure.pem:
  file.managed:
    - source: salt://cloud/cloud.providers.d/azure.pem

/etc/salt/cloud.profiles.d/azure.conf:
  file.managed:
    - source: salt://cloud/cloud.profiles.d/azure.conf

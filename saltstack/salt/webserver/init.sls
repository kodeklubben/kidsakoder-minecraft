install-requirements:
  pip.installed:
    - requirements: /vagrant/requirements.txt

create-log-dir:
  file.directory:
  - name: /var/log/flask
  - user: root
  - group: root
  - dir_mode: 777

# This Salt state sets up the necessary requirements for Celery such as RabbitMQ

### RabbitMQ
# Make sure RabbitMQ is installed
rabbitmq-server:
  pkg.installed:
    - name: rabbitmq-server

  service.running:
    - name: rabbitmq-server
    - enable: True
    - watch:
      - pkg: rabbitmq-server


### Celery
# Celery needs a user for its worker
celery-user:
  user.present:
    - name: celery
    - shell: /bin/bash

# Celery configuration file
celery-config:
  file.managed:
    - name: /etc/default/celeryd
    - source: salt://celery/files/celeryd.conf
    - template: jinja

# Celery daemon init script
celeryd-init:
  file.managed:
    - name: /etc/init.d/celeryd
    - source: salt://celery/files/celeryd
    - mode: 755

  service.running:
    - name: celeryd
    - enable: True
    - require:
      - file: celery-config
    - watch:
      - file: celeryd-init

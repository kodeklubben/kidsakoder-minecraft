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
# Celery configuration file
celery-config:
  file.managed:
    - name: /etc/default/celeryd
    - source: salt://webserver/files/celeryd.conf.j2
    - template: jinja

# Celery daemon init script
celeryd-init:
  file.managed:
    - name: /etc/init.d/celeryd
    - source: salt://webserver/files/celeryd
    - template: jinja
    - mode: 755
  service.running:
    - name: celeryd
    - enable: True
    - require:
      - file: celery-config
    - watch:
      - file: celeryd-init

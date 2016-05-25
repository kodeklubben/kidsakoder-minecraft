# Install apache
install-apache:
  pkg.installed:
    - name: apache2

# Install apache mods
install-apache-mods:
  pkg.installed:
    - name: libapache2-mod-wsgi
  apache_module.enable:
    - name: wsgi

# Remove default apache site
remove-default-apache-site:
  file.absent:
    - name: /etc/apache2/sites-enabled/000-default.conf
    - require:
      - pkg: install-apache

# Setup apache config
apache-config:
  file.managed:
    - name: /etc/apache2/sites-available/kidsakoder.conf
    - source: salt://webserver/files/kidsakoder.conf.j2
    - template: jinja
    - require:
      - pkg: install-apache

# Create symlink to enabled sites instead of doing a2ensite
apache-enable-config:
  file.symlink:
    - name: /etc/apache2/sites-enabled/kidsakoder.conf
    - target: ../sites-available/kidsakoder.conf
    - require:
      - pkg: install-apache

# Make sure apache service
apache-service:
  service.running:
    - name: apache2
    - enable: True
    - restart: True
    - require:
      - pkg: install-apache
    - watch:
      - file: apache-config

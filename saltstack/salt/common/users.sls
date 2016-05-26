# Add user for connecting with public SSH key
add-user:
  user.present:
    - name: {{ pillar['user']['name'] }}
    - shell: {{ pillar['user']['shell'] }}
    - empty_password: True
    - groups:
      - sudo
  # Put the public SSH key in the authorized keys file
  ssh_auth.present:
    - user: {{ pillar['user']['name'] }}
    - source: salt://common/files/kidsakoder.pub
  # Allow sudo without password
  file.managed:
    - name: /etc/sudoers.d/kidsakoder
    - contents:
      - {{ pillar['user']['name'] }} ALL=(ALL) NOPASSWD:ALL


# SSH daemon configuration to limit access
sshd-config:
  file.managed:
    - name: /etc/ssh/sshd_config
    - source: salt://common/files/sshd_config.j2
    - template: jinja

sshd-service:
  service.running:
    - name: ssh
    - enable: True
    - restart: True
    - watch:
      - file: sshd-config


# Make sure Salt Bootstrap user is not enabled.
remove-salt-bootstrap-user:
  user.absent:
    - name: salt-bootstrap

# Add user
add-user:
  user.present:
    - name: {{ pillar['user']['name'] }}
    - shell: {{ pillar['user']['shell'] }}
    - password: {{ pillar['user']['password'] }}
    - groups:
      - {{ pillar['user']['group'] }}

add-user-ssh-key:
  ssh_auth.present:
    - user: {{ pillar['user']['name'] }}
    - names:
      - {{ pillar['user']['ssh-key'] }}


# SSHD Configuration
sshd-allowusers:
  file.managed:
    - name: /etc/ssh/sshd_config
    - source: salt://common/files/sshd_config.j2
    - template: jinja

restart-sshd:
  service.running:
    - name: ssh
    - enable: True
    - restart: True
    - onchanges:
      - file: sshd-allowusers


# Make sure Salt Bootstrap user is not enabled.
remove-salt-bootstrap-user:
  user.absent:
    - name: salt-bootstrap

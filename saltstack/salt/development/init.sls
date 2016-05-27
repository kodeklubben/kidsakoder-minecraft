{% set flask = pillar['flask'] %}

# Add vagrant user to flask group so we can run Flask app from vagrant user
add-vagrant-user-to-flask:
  group.present:
    - name: {{ flask.group }}
    - addusers:
      - vagrant

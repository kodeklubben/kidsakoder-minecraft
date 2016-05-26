# Development only state

# VAGRANT SPECIFIC
# NOTE: Adds vagrant user to flask group so we can run Flask app from vagrant user
add-vagrant-user-to-flask:
  group.present:
    - name: {{ pillar['flask']['group'] }}
    - addusers:
      - vagrant

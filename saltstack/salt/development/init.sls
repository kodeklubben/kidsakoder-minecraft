# This state is only for the development environment

{% set flask = pillar['flask'] %}

# Install testing requirements
install-test-requirements:
  pip.installed:
    - requirements: {{ flask.proj_dir }}/tests/requirements.txt

# Add vagrant user to flask group so we can run Flask app from vagrant user
add-vagrant-user-to-flask:
  group.present:
    - name: {{ flask.group }}
    - addusers:
      - vagrant

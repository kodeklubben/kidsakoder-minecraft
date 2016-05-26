{% set flask = pillar['flask'] %}

# Install testing requirements
install-test-requirements:
  pip.installed:
    - requirements: {{ flask.proj_dir }}/tests/requirements.txt

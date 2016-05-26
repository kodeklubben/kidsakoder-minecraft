# Install ansible
install-ansible:
  pkgrepo.managed:
    - ppa: ansible/ansible
  pkg.installed:
    - name: ansible
    - refresh: True

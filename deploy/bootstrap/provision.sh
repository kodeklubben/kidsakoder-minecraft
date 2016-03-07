#!/bin/bash

# Add SaltStack repository
add-apt-repository ppa:saltstack/salt
# Update to refresh repository
apt-get update --assume-yes
# Install Saltstack
apt-get install --assume-yes salt-master salt-minion salt-cloud
# Start Salt Master
service salt-master start
# Run highstate
salt-call -l debug state.highstate

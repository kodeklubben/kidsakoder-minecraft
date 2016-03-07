#!/bin/bash

# Create Salt configuration directory
mkdir /etc/salt/
# Move Salt configuration
mv /tmp/saltstack/etc/minion.conf /etc/salt/minion
# Move Salt Pillars 
mv /tmp/saltstack/pillar/ /srv/pillar/
# Move Salt States 
mv /tmp/saltstack/salt/ /srv/salt/

# Download SaltStack bootstrap script
wget -O /tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
# Install bootstrap
sh /tmp/bootstrap-salt.sh -L -P stable 

# Run highstate
salt-call --local state.highstate -l debug

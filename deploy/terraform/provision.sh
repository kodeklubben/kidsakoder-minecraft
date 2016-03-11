#!/bin/bash

# Create Salt configuration directory
mkdir /etc/salt/
# Copy Salt configuration
cp -r /tmp/saltstack/etc/* /etc/salt/
# Copy Salt Pillars 
cp -r /tmp/saltstack/pillar/ /srv/pillar/
# Copy Salt States 
cp -r /tmp/saltstack/salt/ /srv/salt/

# Download SaltStack bootstrap script
wget -O /tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
# Install bootstrap
sh /tmp/bootstrap-salt.sh -M -L -P stable 

# Run highstate
salt-call state.highstate -l debug

# Clean up tmp
rm -r /tmp/saltstack
rm /tmp/bootstrap-salt.sh

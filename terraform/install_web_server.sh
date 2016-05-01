#!/bin/bash

# Create Salt configuration directory
mkdir /etc/salt/
# Copy Salt minion configuration
cp /tmp/saltstack/etc/minion.conf /etc/salt/minion
# Copy Salt grains
cp /tmp/grains /etc/salt/grains

# Download SaltStack bootstrap script
wget -O /tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
# Install Salt Minion
sh /tmp/bootstrap-salt.sh -L -P stable 

# Run highstate to get configuration from Salt Master
salt-call state.highstate

# Clean up tmp
rm -r /tmp/saltstack
rm /tmp/bootstrap-salt.sh

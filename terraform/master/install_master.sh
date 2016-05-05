#!/bin/bash

# Create Salt configuration directory
mkdir /etc/salt/
# Copy Salt Master and Minion configuration
cp /tmp/saltstack/etc/master.conf /etc/salt/master
cp /tmp/saltstack/etc/master_minion.conf /etc/salt/minion
# Copy Salt Pillars
cp -r /tmp/saltstack/pillar/ /srv/pillar/
# Copy Salt States
cp -r /tmp/saltstack/salt/ /srv/salt/
# Copy Salt Reactors
cp -r /tmp/saltstack/reactor/ /srv/reactor/

# Copy Azure .pem certificate for Salt Cloud
cp /tmp/saltstack/etc/kidsakoder.pem /etc/salt/kidsakoder.pem

# Download SaltStack bootstrap script
wget -O /tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
# Install SaltStack as master
sh /tmp/bootstrap-salt.sh -M -L -P stable

# Run highstate to get config
salt-call state.highstate

# Clean up tmp
rm -r /tmp/saltstack
rm /tmp/bootstrap-salt.sh

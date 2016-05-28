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

# Download Salt bootstrap script
wget -O /tmp/bootstrap-salt.sh https://bootstrap.saltstack.com
# Install Salt as master
# See https://docs.saltstack.com/en/latest/topics/tutorials/salt_bootstrap.html
sh /tmp/bootstrap-salt.sh -M -L -P stable 2015.8

# Clean up tmp
rm -r /tmp/saltstack
rm /tmp/bootstrap-salt.sh

# Run the Salt states to finish bootstrap
salt-call state.apply

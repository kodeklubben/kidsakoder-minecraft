# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.box = "ubuntu/trusty64"
    master.vm.network "public_network", ip: "192.168.12.100" 
    
    # Saltstack directories 
    master.vm.synced_folder "deploy/saltstack/salt", "/srv/salt"
    master.vm.synced_folder "deploy/saltstack/pillar", "/srv/pillar"

    # Saltstack provisioning
    master.vm.provision "salt" do |salt|
      salt.install_master = true
      salt.install_type = "stable"
      salt.master_config = "deploy/saltstack/etc/master.conf"
      salt.seed_master = {
        master: "deploy/saltstack/vagrant/keys/master.pub",
        web: "deploy/saltstack/vagrant/keys/minion.pub",
        minecraft: "deploy/saltstack/vagrant/keys/minion.pub"
      }
      salt.minion_key = "deploy/saltstack/vagrant/keys/master.pem"
      salt.minion_pub = "deploy/saltstack/vagrant/keys/master.pub"
      salt.minion_config = "deploy/saltstack/vagrant/minion.conf"

      salt.run_highstate = true

      # For debugging 
      salt.verbose = true
      salt.colorize = true
    end
  end

  config.vm.define "web" do |minion|
    minion.vm.hostname = "web"
    minion.vm.box = "ubuntu/trusty64"
    minion.vm.network "public_network", ip: "192.168.12.101"
    minion.vm.network "forwarded_port", guest: 80, host: 8080

    # Saltstack provisioning
    minion.vm.provision "salt" do |salt|
      salt.minion_config = "deploy/saltstack/vagrant/minion.conf"
      salt.minion_key = "deploy/saltstack/vagrant/keys/minion.pem"
      salt.minion_pub = "deploy/saltstack/vagrant/keys/minion.pub"
      salt.run_highstate = true

      # For debugging 
      salt.verbose = true
      salt.colorize = true
    end
  end

  config.vm.define "minecraft" do |minion|
    minion.vm.hostname = "minecraft"
    minion.vm.box = "ubuntu/trusty64"
    minion.vm.network "public_network", ip: "192.168.12.102"

    # Saltstack provisioning
    minion.vm.provision "salt" do |salt|
      salt.minion_config = "deploy/saltstack/vagrant/minion.conf"
      salt.minion_key = "deploy/saltstack/vagrant/keys/minion.pem"
      salt.minion_pub = "deploy/saltstack/vagrant/keys/minion.pub"
      salt.run_highstate = true

      # For debugging 
      salt.verbose = true
      salt.colorize = true
    end
  end

end

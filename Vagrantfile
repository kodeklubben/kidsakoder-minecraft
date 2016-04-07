# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.box = "ubuntu/trusty64"
    master.vm.network "public_network", ip: "192.168.100.100" 
    
    # Saltstack directories 
    master.vm.synced_folder "saltstack/salt", "/srv/salt"
    master.vm.synced_folder "saltstack/pillar", "/srv/pillar"

    # Saltstack provisioning
    master.vm.provision "salt" do |salt|
      salt.install_master = true
      salt.install_type = "stable"
      salt.master_config = "saltstack/etc/master.conf"
      salt.minion_config = "saltstack/etc/master_minion.conf"
      salt.seed_master = {
        master: "saltstack/vagrant/keys/master.pub",
        webserver: "saltstack/vagrant/keys/minion.pub",
        minecraft: "saltstack/vagrant/keys/minion.pub"
      }
      salt.minion_key = "saltstack/vagrant/keys/master.pem"
      salt.minion_pub = "saltstack/vagrant/keys/master.pub"
      salt.run_highstate = true
      salt.colorize = true
      # For debugging 
      # salt.verbose = true
    end

    # Virtualbox settings
    master.vm.provider "virtualbox" do |v|
      v.memory = 256
    end
  end

  config.vm.define "webserver" do |minion|
    minion.vm.hostname = "webserver"
    minion.vm.box = "ubuntu/trusty64"
    minion.vm.network "public_network", ip: "192.168.100.101"
    # Forward port 80 for webserver
    minion.vm.network "forwarded_port", guest: 80, host: 8080

    # Saltstack provisioning
    minion.vm.provision "salt" do |salt|
      salt.minion_config = "saltstack/vagrant/minion.conf"
      salt.minion_key = "saltstack/vagrant/keys/minion.pem"
      salt.minion_pub = "saltstack/vagrant/keys/minion.pub"
      salt.run_highstate = true
      salt.colorize = true
    end
    
    # Virtualbox settings
    minion.vm.provider "virtualbox" do |v|
      v.memory = 256
    end
  end

  config.vm.define "mc" do |minion|
    minion.vm.hostname = "mc"
    minion.vm.box = "ubuntu/trusty64"
    minion.vm.network "public_network", ip: "192.168.100.102"

    # Saltstack provisioning
    minion.vm.provision "salt" do |salt|
      salt.minion_config = "saltstack/vagrant/minion.conf"
      salt.minion_key = "saltstack/vagrant/keys/minion.pem"
      salt.minion_pub = "saltstack/vagrant/keys/minion.pub"
      salt.run_highstate = true
      salt.colorize = true
    end
  end

end

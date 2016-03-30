# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.box = "ubuntu/trusty64"
    master.vm.network "public_network", ip: "192.168.12.100" 
    master.vm.network "forwarded_port", guest: 80, host: 8080
    
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
        minion: "deploy/saltstack/vagrant/keys/minion.pub"
      }

      #salt.run_highstate = true
      # For debugging 
      salt.verbose = true
      salt.colorize = true
    end
  end

  config.vm.define "minion" do |minion|
    minion.vm.hostname = "minion"
    minion.vm.box = "ubuntu/trusty64"
    minion.vm.network "public_network", ip: "192.168.12.101"

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

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "web" do |web|
    web.vm.hostname = "web"
    web.vm.box = "ubuntu/trusty64"
    web.vm.network "public_network"
    web.vm.network "forwarded_port", guest: 80, host: 8080
    
    # Saltstack directories 
    web.vm.synced_folder "deploy/saltstack/salt", "/srv/salt"
    web.vm.synced_folder "deploy/saltstack/pillar", "/srv/pillar"
    web.vm.synced_folder "deploy/saltstack/etc/minion.d", "/etc/salt/minion.d", create: true
    web.vm.synced_folder "deploy/saltstack/etc/master.d", "/etc/salt/master.d", create: true

    # Saltstack provisioning
    web.vm.provision "salt" do |salt|
      salt.install_master = true
      #salt.run_highstate = true
      # For debugging 
      salt.verbose = true
      salt.colorize = true
    end
  end

end

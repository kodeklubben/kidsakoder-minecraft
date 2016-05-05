# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # The Salt master server
  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.box = "ubuntu/trusty64"

    # Network configuration
    ip = "192.168.100.100"
    master.vm.network "private_network", ip: "#{ip}" 
    
    # Post message
    master.vm.post_up_message = "Salt master is up and running at #{ip}\n" \
                                "Use the command 'vagrant ssh master' to connect via SSH."

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
        web: "saltstack/vagrant/keys/minion.pub",
        mc: "saltstack/vagrant/keys/minion.pub"
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
      # Use 512 MB RAM
      v.memory = 512
    end
  end

  # The webserver
  config.vm.define "web" do |minion|
    minion.vm.hostname = "web"
    minion.vm.box = "ubuntu/trusty64"

    # Network configuration
    ip = "192.168.100.101"
    minion.vm.network "private_network", ip: "#{ip}" 
    # Forward port 80 to 8080 for production
    minion.vm.network "forwarded_port", guest: 80, host: 8080
    # Forward port 5000 for debug 
    minion.vm.network "forwarded_port", guest: 5000, host: 5000

    # Post message
    minion.vm.post_up_message = "The web server is up and running at #{ip}.\n" \
                                "Use http://localhost:8080 for port 80.\n" \
                                "Use http://localhost:5050 for port 5000.\n" \
                                "Use the command 'vagrant ssh web' to connect via SSH."

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
      # Use 1024 MB RAM
      v.memory = 1024
    end
  end

  # The Minecraft server
  config.vm.define "mc" do |minion|
    minion.vm.hostname = "mc"
    minion.vm.box = "ubuntu/trusty64"
    
    # Network configuration
    ip = "192.168.100.102"
    minion.vm.network "private_network", ip: "#{ip}"
    # Forward port 25565 for Minecraft
    minion.vm.network "forwarded_port", guest: 25565, host: 25565

    # Post message
    minion.vm.post_up_message = "The Minecraft Forge server is up and running at #{ip}.\n" \
                                "Connect to localhost:25565 or #{ip}:25565 to play.\n" \
                                "Use the command 'vagrant ssh mc' to connect via SSH."

    # Saltstack grains 
    minion.vm.provision "shell", run: "always", inline: <<-SHELL
      mkdir /etc/salt/
      echo 'forge_version: 189' > /etc/salt/grains
      echo 'mod: raspberryjam' >> /etc/salt/grains
      echo 'raspberryjam_version: 0.52' >> /etc/salt/grains
      echo 'size: small' >> /etc/salt/grains
    SHELL

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
      # Use 1024 MB RAM
      v.memory = 1024
    end
  end

end

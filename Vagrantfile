# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # MASTER SERVER
  config.vm.define "master" do |master|
    # Define the hostname of the machine
    master.vm.hostname = "master"

    # Use Ubuntus box
    master.vm.box = "ubuntu/trusty64"

    # Network configuration
    master.vm.network "private_network", ip: "192.168.100.100"
    # Forward port 80 to 8080 for production
    master.vm.network "forwarded_port", guest: 80, host: 8080
    # Forward port 5000 for debug
    master.vm.network "forwarded_port", guest: 5000, host: 5000

    master.ssh.forward_agent = true

    # Sync project directory
    master.vm.synced_folder ".", "/vagrant"
    master.vm.synced_folder ".", "/opt/kidsakoder-minecraft"

    # Salt directories
    master.vm.synced_folder "saltstack/salt", "/srv/salt"
    master.vm.synced_folder "saltstack/pillar", "/srv/pillar"
    master.vm.synced_folder "saltstack/reactor", "/srv/reactor"

    # Salt provisioning
    master.vm.provision "salt" do |salt|
      # Salt install configuration
      salt.install_master = true
      # Use stable Salt version 2015.8
      salt.install_type = "stable"
      salt.install_args = "2015.8"

      # Salt master configuration
      salt.master_config = "saltstack/etc/master.conf"

      # Grain that sets special settings for Vagrant development.
      # See grains file and saltstack/salt/top.sls for more info.
      salt.grains_config = "saltstack/vagrant/grains/master"

      # Minion config
      salt.minion_config = "saltstack/etc/master_minion.conf"

      # Define keys for master and mc machines
      salt.master_key = "saltstack/vagrant/keys/master.pem"
      salt.master_pub = "saltstack/vagrant/keys/master.pub"
      salt.minion_key = "saltstack/vagrant/keys/master.pem"
      salt.minion_pub = "saltstack/vagrant/keys/master.pub"
      salt.seed_master = {
        master: "saltstack/vagrant/keys/master.pub",
        mc: "saltstack/vagrant/keys/minion.pub"
      }

      # Apply states on start
      salt.run_highstate = true
      salt.colorize = true

      # Enable for debugging
      # salt.verbose = true
      # salt.log_level = "warning"
    end

    # Virtualbox settings
    master.vm.provider "virtualbox" do |v|
      v.memory = 1024
    end

    # Post message
    master.vm.post_up_message = "The Salt master and web server is up and running.\n" \
                                "Use http://localhost:8080 for port 80.\n" \
                                "Use http://localhost:5000 for port 5000.\n"
  end


  # MINECRAFT SERVER
  config.vm.define "mc" do |minion|
    # Define the hostname of the machine
    minion.vm.hostname = "mc"

    # Use Ubuntus box
    minion.vm.box = "ubuntu/trusty64"

    # Network configuration
    minion.vm.network "private_network", ip: "192.168.100.101"
    # Forward port 25565 for Minecraft
    minion.vm.network "forwarded_port", guest: 25565, host: 25565

    # Salt provisioning
    minion.vm.provision "salt" do |salt|
      # Use stable Salt version 2015.8
      salt.install_type = "stable"
      salt.install_args = "2015.8"

      # Grain that defines this to be a Minecraft server.
      # See grains file and saltstack/salt/top.sls for more info.
      salt.grains_config = "saltstack/vagrant/grains/mc"

      # Minion config
      salt.minion_config = "saltstack/vagrant/minion.conf"

      # Minion keys
      salt.minion_key = "saltstack/vagrant/keys/minion.pem"
      salt.minion_pub = "saltstack/vagrant/keys/minion.pub"

      # Apply states on start
      salt.run_highstate = true
      salt.colorize = true

      # Enable for debugging
      # salt.verbose = true
      # salt.log_level = "warning"
    end

    # Virtualbox settings
    minion.vm.provider "virtualbox" do |v|
      v.memory = 1024
    end

    # Post message
    minion.vm.post_up_message = "The Minecraft Forge server is up and running.\n" \
                                "See saltstack/vagrant/grains/mc for which versions of Forge and ComputerCraft.\n" \
                                "Connect to localhost:25565 in Minecraft to play.\n"
  end
end

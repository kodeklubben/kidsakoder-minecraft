# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  # The Salt master server
  config.vm.define "master" do |master|
    master.vm.hostname = "master"
    master.vm.box = "ubuntu/trusty64"

    # Network configuration
    master.vm.network "private_network", ip: "192.168.100.100"
    # Forward port 80 to 8080 for production
    master.vm.network "forwarded_port", guest: 80, host: 8080
    # Forward port 5000 for debug
    master.vm.network "forwarded_port", guest: 5000, host: 5000

    # Sync project directory
    master.vm.synced_folder ".", "/vagrant"
    master.vm.synced_folder ".", "/opt/kidsakoder-minecraft"

    # Salt directories
    master.vm.synced_folder "saltstack/salt", "/srv/salt"
    master.vm.synced_folder "saltstack/pillar", "/srv/pillar"
    master.vm.synced_folder "saltstack/reactor", "/srv/reactor"

    # Salt provisioning
    master.vm.provision "salt" do |salt|
      salt.install_master = true
      salt.install_type = "stable"
      salt.master_config = "saltstack/etc/master.conf"
      salt.minion_config = "saltstack/etc/master_minion.conf"
      salt.seed_master = {
        master: "saltstack/vagrant/keys/master.pub",
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
      v.memory = 1024
    end

    # Post message
    master.vm.post_up_message = "The Salt master and web server is up and running.\n" \
                                "Use http://localhost:8080 for port 80.\n" \
                                "Use http://localhost:5000 for port 5000.\n"
  end


  # The Minecraft server
  config.vm.define "mc" do |minion|
    minion.vm.hostname = "mc"
    minion.vm.box = "ubuntu/trusty64"

    # Network configuration
    minion.vm.network "private_network", ip: "192.168.100.101"
    # Forward port 25565 for Minecraft
    minion.vm.network "forwarded_port", guest: 25565, host: 25565

    # Salt Grains
    # This creates a static grains file when running vagrant up or vagrant provision
    # which defines which versions of Forge and ComputerCraft should be installed.
    # The size used (very small) defines how much memory the Java process uses.
    minion.vm.provision "shell", run: "always", inline: <<-SHELL
      mkdir /etc/salt/
      echo 'forge_version: 189' > /etc/salt/grains
      echo 'computercraft_version: 179' >> /etc/salt/grains
      echo 'size: verysmall' >> /etc/salt/grains
    SHELL

    # Salt provisioning
    minion.vm.provision "salt" do |salt|
      salt.minion_config = "saltstack/vagrant/minion.conf"
      salt.minion_key = "saltstack/vagrant/keys/minion.pem"
      salt.minion_pub = "saltstack/vagrant/keys/minion.pub"
      salt.run_highstate = true
      salt.colorize = true
    end

    # Virtualbox settings
    minion.vm.provider "virtualbox" do |v|
      v.memory = 1024
    end

    # Post message
    minion.vm.post_up_message = "The Minecraft Forge server is up and running.\n" \
                                "Connect to localhost:25565 to play.\n"
  end

end

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/focal64"

    config.vm.provider "virtualbox" do |provider|
      provider.memory = 1024
      provider.cpus = 2
    end

    config.vm.provision "shell", inline: <<-SHELL
      set -x
      apt-get update

      apt-get install -y git python-is-python3

      git clone https://github.com/fwilhe2/mininet
      mininet/util/install.sh -a

      curl -s -L https://github.com/mhausenblas/cinf/releases/latest/download/cinf_linux_amd64.tar.gz \
       -o cinf.tar.gz && \
       tar xvzf cinf.tar.gz cinf && \
       mv cinf /usr/local/bin && \
       rm cinf*


    SHELL
end

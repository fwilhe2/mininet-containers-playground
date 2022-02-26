# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/focal64"

    config.vm.provision "shell", inline: <<-SHELL
      apt-get update

      apt-get install -y mininet python-is-python3
      
      curl -s -L https://github.com/mhausenblas/cinf/releases/latest/download/cinf_linux_amd64.tar.gz \
       -o cinf.tar.gz && \
       tar xvzf cinf.tar.gz cinf && \
       mv cinf /usr/local/bin && \
       rm cinf*


    SHELL
end

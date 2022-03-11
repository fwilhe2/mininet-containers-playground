# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/focal64"

    config.vm.provider "virtualbox" do |provider|
      provider.memory = 1024
      provider.cpus = 2
    end

    config.vm.provision "file", source: "tmux.conf", destination: "~/.tmux.conf"
    config.vm.provision "file", source: "hosts", destination: "hosts"

    config.vm.provision "shell", inline: <<-SHELL
      set -x
      apt-get update

      cp hosts /etc/hosts

      apt-get install -y git python-is-python3 golang httpie traceroute

      git clone https://github.com/fwilhe2/mininet
      mininet/util/install.sh -a

      curl -s -L https://github.com/mhausenblas/cinf/releases/latest/download/cinf_linux_amd64.tar.gz \
       -o cinf.tar.gz && \
       tar xvzf cinf.tar.gz cinf && \
       mv cinf /usr/local/bin && \
       rm cinf*

      pushd /vagrant/go-server
      go build .
      mv go-server /usr/local/bin/
      popd

      apt-get update
      apt-get install -y apt-transport-https gnupg2 curl lsb-release
      curl -sL 'https://deb.dl.getenvoy.io/public/gpg.8115BA8E629CC074.key' | gpg --dearmor -o /usr/share/keyrings/getenvoy-keyring.gpg
      echo a077cb587a1b622e03aa4bf2f3689de14658a9497a9af2c427bba5f4cc3c4723 /usr/share/keyrings/getenvoy-keyring.gpg | sha256sum --check
      echo "deb [arch=amd64 signed-by=/usr/share/keyrings/getenvoy-keyring.gpg] https://deb.dl.getenvoy.io/public/deb/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/getenvoy.list
      apt-get update
      apt-get install -y getenvoy-envoy

    SHELL
end

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
   config.vm.define "machine1" do |machine1| 
      machine1.vm.box = "ubuntu/bionic64"
      machine1.vm.network "private_network", ip: "192.168.33.10"
      machine1.vm.network "forwarded_port", guest: 8000, host: 8000
      machine1.vm.network "forwarded_port", guest: 30010, host: 30010
      machine1.vm.network "forwarded_port", guest: 30011, host: 30011
      machine1.vm.network "forwarded_port", guest: 30012, host: 30012

      machine1.vm.provision "file", source: "./kube-setup/kube-prometheus-stack", destination: "$HOME/kube-prometheus-stack"
      machine1.vm.provision "file", source: "./kube-setup/kube-flannel.yml", destination: "$HOME/kube-flannel.yml"
      machine1.vm.provision "file", source: "./kube-setup/part1.sh", destination: "$HOME/part1.sh"
      machine1.vm.provision "file", source: "./kube-setup/part2_master.sh", destination: "$HOME/part2_master.sh"
      machine1.vm.provision "file", source: "./src", destination: "$HOME/src"
      machine1.vm.provision "file", source: "./chaos-tests", destination: "$HOME/chaos-tests"

      machine1.vm.provider "virtualbox" do |m1_vb|
         m1_vb.memory = "2048"
         m1_vb.cpus = 2
      end
   end 

   config.vm.define "machine2" do |machine2| 
      machine2.vm.box = "ubuntu/bionic64"
      machine2.vm.network "private_network", ip: "192.168.33.11"
      machine2.vm.network "forwarded_port", guest: 8001, host: 8001

      machine2.vm.provision "file", source: "./kube-setup/part1.sh", destination: "$HOME/part1.sh"

      machine2.vm.provider "virtualbox" do |m2_vb|
         m2_vb.memory = "2048"
         m2_vb.cpus = 1
      end
   end 

   config.vm.define "machine3" do |machine3| 
      machine3.vm.box = "ubuntu/bionic64"
      machine3.vm.network "private_network", ip: "192.168.33.12"
      machine3.vm.network "forwarded_port", guest: 8002, host: 8002
      
      machine3.vm.provision "file", source: "./kube-setup/part1.sh", destination: "$HOME/part1.sh"

      machine3.vm.provider "virtualbox" do |m3_vb|
         m3_vb.memory = "2048"
         m3_vb.cpus = 1
      end
   end 
end

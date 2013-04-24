# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "_precise64"
  config.vm.box_url =  "http://files.vagrantup.com/precise64.box"

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  end

  # make sure to install vagrant-aws plugin
  # $ vagrant plugin install vagrant-aws 
  config.vm.provider :aws do |aws, override|
    # todo: read this in from a file that is not checked into git
    aws.access_key_id = "AKIAJ6PF5PWHFME4GA5A"
    aws.secret_access_key = "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"
    aws.keypair_name = "trivio deploy key"
    aws.security_groups = ["blink", "default"]
    aws.ami = "ami-7747d01e"
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = "keys/moz.rsa"

  end
 
  # make sure you add the vagrant omnibus plugin
  # $ vagrant plugin install vagrant-omnibus 
  config.omnibus.chef_version = :latest
 
  config.vm.provision :chef_solo do |chef|
    chef.cookbooks_path = "chef/cookbooks"
    chef.add_recipe("web")
    chef.add_recipe("web::nginx_flask")
  end

end

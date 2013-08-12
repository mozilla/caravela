# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  config.vm.box_url =  "http://files.vagrantup.com/precise64.box"

  config.vm.box = "_precise64"
  config.vm.provider :virtualbox do |vb|
    
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    config.vm.synced_folder "~/Projects/trivio.client", "/src/trivio.client"
    config.vm.synced_folder "~/Projects/trivio.datasources", "/src/trivio.datasources"
    
    config.vm.synced_folder "~/Projects/leisure", "/src/leisure"
    config.vm.synced_folder "~/Projects/codd", "/src/codd"

    config.vm.synced_folder "~/Projects/splicer", "/src/splicer"
    config.vm.synced_folder "~/Projects/splicer_discodb", "/src/splicer_discodb"
    config.vm.synced_folder "~/Projects/splicer_console", "/src/splicer_console"

    config.vm.network :forwarded_port, guest: 80, host: 5000
  end

  # make sure to install vagrant-aws plugin
  # $ vagrant plugin install vagrant-aws 
  config.vm.provider :aws do |aws, override|
    override.vm.box = "dummy"
    # todo: read this in from a file that is not checked into git
    aws.access_key_id = ENV['AWS_KEY']
    aws.secret_access_key = ENV['AWS_SECRET']
    aws.keypair_name = "trivio deploy key"
    aws.security_groups = ["blink", "default"]
    aws.ami = "ami-7747d01e"
    aws.instance_type = "m1.xlarge"
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
    chef.add_recipe("web::rabbitmq")

  end

end

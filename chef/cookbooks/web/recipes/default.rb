
bash "apt update" do
  code "apt-get update"
end

package "git"
package "python-pip"
package "python-dev"
package "libcmph-dev"
package "python-mysqldb"
package "libxml2-dev"
package "libxslt-dev"
package "libmysqld-dev"
package "libevent-dev"

package "rabbitmq-server"


directory "/srv/" do
  action :create
  owner node[:app][:user]
  group node[:app][:user]
end

bash "virtualenv" do
  code "pip install virtualenv>=1.9.1"
  not_if "which virtualenv"
end

bash "setup" do
  user  node[:app][:user]
  group node[:app][:user]
  #flags "-l" # bash -l use full login environment
  environment "HOME"=>node[:app][:home]

  code <<-EOF
  virtualenv  --distribute /srv/#{node[:app][:name]}
  . /srv/#{node[:app][:name]}/bin/activate
  pip install -r #{node[:app][:home]}/web/requirements.txt
  EOF
end

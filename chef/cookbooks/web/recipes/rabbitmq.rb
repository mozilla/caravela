package "rabbitmq-server"


bash "Create rabbitmq user and vhost" do
  code <<-EOF
  rabbitmqctl add_user #{node[:app][:user]} mypasswd
  rabbitmqctl add_vhost /#{node[:app][:name]}
  rabbitmqctl set_permissions -p /#{node[:app][:name]} #{node[:app][:user]} ".*" ".*" ".*"
  EOF
end

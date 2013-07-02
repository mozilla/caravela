package "build-essential"
package "nginx"


USER = node[:app][:user]
user USER



# setup nginx
template "/etc/nginx/sites-enabled/default" do
  mode 00644
  source "blink.nginx.erb"
  notifies :reload, "service[nginx]"
end

service "nginx" do
  supports :restart => true, :reload => true, :start => true, :enable => true
  action [ :enable, :start ]
end


gem_package "foreman"


bash "create/update upstart scripts" do
  cwd "#{node[:app][:home]}"
  code "foreman export --app #{node[:app][:name]} --user #{USER} upstart /etc/init -d #{node[:app][:home]}"
end


service "#{node[:app][:name]}" do
  provider Chef::Provider::Service::Upstart
  enabled true
  running true
  supports :restart => true, :reload => true, :status => true
  action [:enable, :start]
end




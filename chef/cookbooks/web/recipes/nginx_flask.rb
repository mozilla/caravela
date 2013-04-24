package "build-essential"
package "nginx"
USER = "ubuntu"
#user USER

bash "Install python requirements" do
  
  code <<-EOH
    pip install distribute==0.6.28
    pip install gunicorn
  EOH

end

template "/etc/blink.cfg" do
  mode 00644
  source "blink.cfg.erb"
end


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


# configure gunicorn

directory "/var/log/blink" do
  mode 00755
  owner USER
end


template "/etc/init/blink.conf" do
  mode 00644
  source "blink.upstart.erb"
  notifies  :reload, "service[blink]"
end

service "blink" do
  provider Chef::Provider::Service::Upstart
  enabled true
  running true
  supports :restart => true, :reload => true, :status => true
  action [:enable, :start]
end




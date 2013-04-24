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

bash "setup" do
  code <<-EOF
  #sudo pip install virtualenv
  cd /vagrant/site
  pip install -r requirements.txt
  EOF
end

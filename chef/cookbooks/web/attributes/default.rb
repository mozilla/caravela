# silly hack to determine wether we're using the aws provider
# or the virtualbox one
if File.readlines("/etc/passwd").grep(/ubuntu/).size > 0
  default["app"]["user"] = "ubuntu"
else
  default["app"]["user"] = "vagrant"
end


default["app"]["home"] = "/vagrant"
default["app"]["name"] = "caravela"



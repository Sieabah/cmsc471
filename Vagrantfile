Vagrant.configure(2) do |config|
  config.vm.box = "debian/contrib-jessie64"

  config.vm.synced_folder '.', '/vagrant', disabled: true
  config.vm.synced_folder "./proj3/", "/vagrant", create: true

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y texlive
  SHELL
end

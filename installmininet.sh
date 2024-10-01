sudo apt update -y
sudo apt upgrade -y
sudo apt install net-tools -y
sudo apt-get install curl -y
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest -y
git clone https://github.com/mininet/mininet
cd mininet
git checkout -b mininet-2.3.0 2.3.0
util/install.sh
cd ..
sudo apt-get install openvswitch-switch
sudo service openvswitch-switch start
git clone https://github.com/intrig-unicamp/mininet-wifi
cd mininet-wifi
sudo util/install.sh -Wlnfv
cd ..
sudo pip install pandas openpyxl
sudo pip uninstall numpy
sudo pip install numpy==1.22.4
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils -y
sudo apt install virt-manager -y
sudo adduser $(whoami) libvirt
sudo adduser $(whoami) kvm
wget https://raw.githubusercontent.com/pimlie/ubuntu-mainline-kernel.sh/master/ubuntu-mainline-kernel.sh
sudo install ubuntu-mainline-kernel.sh /usr/local/bin/
sudo ubuntu-mainline-kernel.sh -c   
sudo ubuntu-mainline-kernel.sh -i



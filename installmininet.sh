sudo apt update
sudo apt upgrade
sudo apt install net-tools
sudo apt-get install curl
curl -s https://packagecloud.io/install/repositories/ookla/speedtest-cli/script.deb.sh | sudo bash
sudo apt-get install speedtest
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


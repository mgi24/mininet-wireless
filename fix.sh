sudo ip link set virbr1 up
dhclient virbr1
sudo echo 'nameserver 8.8.8.' > /etc/resolv.conf
git pull
sudo mn -c
sudo python test2.py
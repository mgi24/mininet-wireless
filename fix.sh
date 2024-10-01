sudo ip link set virbr1 up
dhclient virbr1
git pull
sudo mn -c
sudo python test2.py
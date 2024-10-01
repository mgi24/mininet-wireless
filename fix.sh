sudo ip link set virbr0 up
dhclient virbr0
git pull
sudo mn -c
sudo python test2.py
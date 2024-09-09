#!/usr/bin/env python

'This example creates a simple network topology with 1 AP and 2 stations'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller,  Host,  OVSKernelSwitch
from mininet.link import Intf
from random import uniform
import json
import time
import matplotlib.pyplot as plt

def pinghost(net, host1, host2):
    h1 = net.get(host1)
    h2 = net.get(host2)

    if h1 and h2:
        h1_ip_output = h1.cmd('hostname -I')
        h1_ip_list = h1_ip_output.split()
        h2_ip_output = h2.cmd('hostname -I')
        h2_ip_list = h2_ip_output.split()
        
        if h1_ip_list and h2_ip_list:
            h1_ip = h1_ip_list[0]
            h2_ip = h2_ip_list[0]
            result = h1.cmd(f'ping -c 4 {h2_ip}')
        else:
            print("Failed to retrieve IP for h1 or h2")
        print(result)
        print(f"Host {host1} or {host2} not found")

class CustomCLI(CLI):
    def do_pinghost(self, line):
        "Ping test: pinghost <host1> <host2>"
        args = line.split()
        if len(args) != 2:
            print("Usage: pinghost <host1> <host2>")
            return
        host1 = args[0]
        host2 = args[1]
        pinghost(self.mn, host1, host2)
    
    def do_speedtest(self, line):
        "Run speedtest on all STAs"
        sta_list = self.mn.stations
        if sta_list:
            print("removing previous run json...")
            sta_list[0].cmd('rm -f speedtest*')
            print("starting speedtest...")

            for i, sta in enumerate(sta_list):
                if i == len(sta_list) - 1:
                    sta.cmd(f"speedtest -s 33207 --format json > speedtest{sta.name}.json")
                else:
                    sta.cmd(f"speedtest -s 33207 --format json > speedtest{sta.name}.json &")
            
            print("waiting for speedtest to finish...")
            time.sleep(10)
            print("formating json to be more readable...")

            upload_speeds = []
            download_speeds = []

            for sta in sta_list:
                result_file = f'speedtest{sta.name}.json'
                with open(result_file) as f:
                    data = json.load(f)
                    data['download']['bandwidth'] *= 8
                    data['upload']['bandwidth'] *= 8
                    upload_speeds.append(data['upload']['bandwidth'])
                    download_speeds.append(data['download']['bandwidth'])
                    data_str = json.dumps(data, indent=4)
                    print(f"Speedtest result on {sta.name}:")
                    print(data_str)

            total_upload_speed = sum(upload_speeds)
            total_download_speed = sum(download_speeds)
            print(f"Total upload speed: {total_upload_speed}")
            print(f"Total download speed: {total_download_speed}")
            

            plt.figure()
            plt.plot(upload_speeds, label='Upload Speed')
            plt.plot(download_speeds, label='Download Speed')
            plt.axhline(y=total_upload_speed, color='r', linestyle='--', label='Total Upload Speed')
            plt.axhline(y=total_download_speed, color='g', linestyle='--', label='Total Download Speed')
            plt.xlabel('Station')
            plt.ylabel('Speed (Mbps)')
            plt.title('Upload and Download Speeds')
            plt.legend()
            plt.show()

            
        else:
            print("No STAs found")
        
    def do_stalist(self, line):
        "Print all available STAs"
        sta_list = self.mn.stations
        if sta_list:
            for sta in sta_list:
                print(sta.name)
        else:
            print("No STAs found")
        
            
        
def generate_random_position(ap_position, radius):
    x_ap, y_ap, z_ap = ap_position
    # Generate random offset within the radius
    x_offset = uniform(-radius, radius)
    y_offset = uniform(-radius, radius)
    return (x_ap + x_offset, y_ap + y_offset, z_ap)


def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    ap1 = net.addAccessPoint('ap1', ssid="simpletopo", mode="n",
                             channel="36", position='50.0,50.0,0.0')
    
    info("*** Adding STAs\n")
    ap_position = (50, 50, 0)
    sta_count = int(input("Enter the number of stations to add: "))
    radius = 10
    stations = []
    for i in range (sta_count):
        sta_name = f'sta{i+1}'
        sta_position = generate_random_position(ap_position, radius)
        sta = net.addStation(sta_name,ip='0.0.0.0' ,position=sta_position, mode = "n", channel = "36")
        stations.append(sta)
        print(f"Added {sta_name} at position {sta_position}")
    
    info("*** Simulating Interference\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    h1 = net.addHost('h1', ip = '0.0.0.0')
    h2 = net.addHost('h2', ip = '0.0.0.0')
    
    c0 = net.addController('c0')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info('*** Adding physical interface ens33 >===< switch\n')
    intf = Intf('ens33', node=s1)
    
    info("*** Connecting Stations to AP\n")
    for i, sta in enumerate(stations):
        sta.setAssociation(ap1, intf=f'{sta.name}-wlan0')
    
    info("*** Wiring up switch\n")
    net.addLink(s1, ap1)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    
    info("*** Plotting Graph\n")
    net.plotGraph( min_x=0, max_x=70,min_y = 0, max_y=80)
    
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    s1.start([c0])

    info("*** Getting IP's from DHCP\n")
    h1.cmd('dhclient h1-eth0')
    h2.cmd('dhclient h2-eth0')
    print(stations)
    for i, sta in enumerate(stations):
        sta.cmd(f'dhclient {sta.name}-wlan0')
        ip_output = sta.cmd('hostname -I')
        ip_list = ip_output.split()
        if ip_list:
            print(f"IP {sta.name}: {ip_list[0]}")
        else:
            print(f"Failed to retrieve IP for {sta.name}")
        
    print(f"IP h1:{h1.cmd('hostname -I')}")
    print(f"IP h2:{h2.cmd('hostname -I')}")
    
    info("*** Setting DNS up\n")
    h1.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
    
    

    
    info("*** Running Custom CLI\n")
    CustomCLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
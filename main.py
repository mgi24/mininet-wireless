#!/usr/bin/env python

'This example shows how to work with authentication'
from random import uniform
from mn_wifi.link import wmediumd
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.node import Controller,  Host,  OVSKernelSwitch
from mininet.link import Intf
from mn_wifi.node import Station, OVSKernelAP
import time
import json
import matplotlib.pyplot as plt

def generate_random_position(ap_position, radius):
    x_ap, y_ap, z_ap = ap_position
    # Generate random offset within the radius
    x_offset = uniform(-radius, radius)
    y_offset = uniform(-radius, radius)
    return (x_ap + x_offset, y_ap + y_offset, z_ap)


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    h1 = net.addHost('h1', ip = '0.0.0.0')
    h2 = net.addHost('h2', ip = '0.0.0.0')
    
    info("*** Adding STAs\n")
    
    ap_position = (50, 50, 0)
    sta_count = int(input("Enter the number of stations to add: "))
    radius = 10
    stations = []
    for i in range (sta_count):
        sta_name = f'sta{i+1}'
        sta_position = generate_random_position(ap_position, radius)
        sta = net.addStation(sta_name,ip='0.0.0.0' ,position=sta_position)
        stations.append(sta)
        print(f"Added {sta_name} at position {sta_position}")


    #ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="n", channel="11", position='50.0,50.0,0.0')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid',
                             channel='1', mode='g', position='50.0,50.0,0.0')
    net.setPropagationModel(model="logDistance", exp=3.0)
    
    c0 = net.addController('c0')
    
    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    #net.addLink(sta1, ap1)
    #net.addLink(sta2, ap1)
    net.addLink(s1, ap1)
    net.addLink(s1, h1)
    net.addLink(s1, h2)

    info('*** Adding physical interface ens33 >===< switch\n')
    intf = Intf('ens33', node=s1)

    info("*** Plotting Graph\n")
    net.plotGraph(max_x=120, max_y=120)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    s1.start([c0])

    ap1.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
    h1.cmd('dhclient h1-eth0')
    h2.cmd('dhclient h2-eth0')

    info('*** leasing IP from DHCP Server, if too long comment below!\n')
    print(stations)
    for i, sta in enumerate(stations):
        sta.cmd(f'dhclient {sta.name}-wlan0')
        print(f"IP {sta.name}:{sta.cmd('hostname -I')}")

    info('*** Checking IP address host\n')
    print(f"IP h1:{h1.cmd('hostname -I')}")
    print(f"IP h2:{h2.cmd('hostname -I')}")

    info('*** Changing DNS server\n')
    h1.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
    h1.cmd("rm speedtest*")
    info('*** Speedtest Testing on Backround\n')
    for i, sta in enumerate(stations):
        
        sta.cmd(f'speedtest -s 13777 --format=json > speedtest{sta.name}.json &')

    
    time.sleep(50)
    
    # Read and format JSON files
    info('*** Speedtest Results\n')

        

    # Initialize lists to store upload and download speeds
    upload_speeds = []
    download_speeds = []

    # Read and format JSON files
    for i, sta in enumerate(stations):
        result_file = f'speedtest{sta.name}.json'
        with open(result_file) as f:
            data = json.load(f)
            data['download']['bandwidth'] *= 8
            data['upload']['bandwidth'] *= 8
            upload_speeds.append(data['upload']['bandwidth'])
            download_speeds.append(data['download']['bandwidth'])

    # Plot the upload and download speeds
    # Calculate total speed
    total_upload_speed = sum(upload_speeds)
    total_download_speed = sum(download_speeds)

    # Plot the upload and download speeds
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

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
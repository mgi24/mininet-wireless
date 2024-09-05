#!/usr/bin/env python

'This example shows how to work with authentication'

from mn_wifi.link import wmediumd
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.node import Controller,  Host,  OVSKernelSwitch
from mininet.link import Intf

def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    h1 = net.addHost('h1', ip = '0.0.0.0')
    h2 = net.addHost('h2', ip = '0.0.0.0')
    

    sta1 = net.addStation('sta1', ip = '0.0.0.0',  position = '60.0,60.0,0.0')
    sta2 = net.addStation('sta2', ip = '0.0.0.0', position = '0.0,60.0,0.0')
    ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="g", channel="1", position = '20.0,60.0,0.0')
    net.setPropagationModel(model="logDistance", exp=3.0)
    
    c0 = net.addController('c0')
    
    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)
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
    sta1.cmd('dhclient sta1-wlan0')
    sta2.cmd('dhclient sta2-wlan0')

    info('*** Checking IP address host\n')
    print(f"IP h1:{h1.cmd('hostname -I')}")
    print(f"IP h2:{h2.cmd('hostname -I')}")
    print(f"IP sta1:{sta1.cmd('hostname -I')}")
    print(f"IP sta2:{sta2.cmd('hostname -I')}")
    info('*** Changing DNS server\n')
    h1.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
    
    

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
#!/usr/bin/env python

'This example shows how to work with authentication'

from mn_wifi.link import wmediumd
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.node import Controller,  Host,  OVSKernelSwitch


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    h1 = net.addHost('h1', ip = '192.168.1.125/24')
    h2 = net.addHost('h2', ip = '192.168.1.130/24')
    

    sta1 = net.addStation('sta1', ip = '192.168.1.120/24',  position = '100.0,60.0,0.0')
    sta2 = net.addStation('sta2', ip = '192.168.1.122/24', position = '0.0,60.0,0.0')


    ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="g", channel="1", position = '20.0,60.0,0.0')
    c0 = net.addController('c0')
    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    #net.addLink(sta1, ap1)
    #net.addLink(sta2, ap1)
    net.addLink(s1, ap1)
    net.addLink(s1, h1)
    net.addLink(s1, h2)

    info("*** Plotting Graph\n")
    net.plotGraph(max_x=120, max_y=120)

    info("*** Starting network\n")
    net.build()
    ap1.start([c0])
    s1.start([c0])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
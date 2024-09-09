#!/usr/bin/env python

'This example shows how to work with authentication'

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import wmediumd

from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip = '192.168.1.1/24', passwd='123456789a', encrypt='wpa2',position='10,10,0', mode ='n', channel = '36')
    sta2 = net.addStation('sta2', ip = '192.168.1.2/24', passwd='123456789a', encrypt='wpa2',position='10,10,0', mode ='n', channel = '36')
    ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="n", channel="36",
                             passwd='123456789a', encrypt='wpa2',
                             failMode="standalone", datapath='user',position='10,10,0')
    net.setPropagationModel(model="logDistance", exp=1.0)
    
    c0 = net.addController('c0')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    #net.addLink(sta1, ap1)
    #net.addLink(sta2, ap1)
    sta1.setAssociation(ap1, intf='sta1-wlan0')
    sta2.setAssociation(ap1, intf='sta2-wlan0')
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
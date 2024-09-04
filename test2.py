#!/usr/bin/env python

'This example shows how to work with authentication'

from mn_wifi.link import wmediumd
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi(link=wmediumd)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip = '192.168.1.120/24')
    sta2 = net.addStation('sta2', ip = '192.168.1.122/24')
    ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="g", channel="1",
                             
                             failMode="standalone")
    c0 = net.addController('c0')
    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    info("*** Starting network\n")
    net.build()
    ap1.start([c0])

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
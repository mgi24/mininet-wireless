#!/usr/bin/env python

'This example creates a simple network topology with 1 AP and 2 stations'

import sys

from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")


    ap1 = net.addAccessPoint('ap1', ssid="simpletopo", mode="g",
                             channel="5", )
    sta1 = net.addStation('sta1', ip = '192.168.1.102/24')
    sta2 = net.addStation('sta2', ip = '192.168.1.105/24')
    c0 = net.addController('c0')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info("*** Associating Stations\n")
    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

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
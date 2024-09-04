#!/usr/bin/env python

'This example creates a simple network topology with 1 AP and 2 stations'

import sys

from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf


def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    sta_arg, ap_arg = {}, {}
    if '-v' in sys.argv:
        sta_arg = {'nvif': 2}
    else:
        # isolate_clientes: Client isolation can be used to prevent low-level
        # bridging of frames between associated stations in the BSS.
        # By default, this bridging is allowed.
        # OpenFlow rules are required to allow communication among nodes
        ap_arg = {'client_isolation': True}

    ap1 = net.addAccessPoint('ap1', ssid="simpletopo", mode="g",
                             channel="5", **ap_arg)
    c0 = net.addController('c0')

    info("*** Menambahkan switch\n")
    s1 = net.addSwitch('s1')

    info("*** Menambahkan host\n")
    h1 = net.addHost('h1', ip='0.0.0.0')


    
    info("*** Menghubungkan switch ke interface fisik ens33\n")
    #Intf('ens33', node=s1)
    h2 = net.addHost('h2', ip = '192.168.1.1/24')
    

    info("*** Configuring nodes\n")
    net.configureNodes()
    info("*** Menghubungkan switch ke host\n")
    net.addLink(s1, h1)

    info("*** Menghubungkan switch ke access point\n")
    net.addLink(s1, ap1)
    net.addLink(s1,h2)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    s1.start([c0])
    

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()





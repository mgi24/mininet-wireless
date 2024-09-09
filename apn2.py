#!/usr/bin/python

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from subprocess import call


def myNetwork():

    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6653)

    info( '*** Add switches/APs\n')
    ap1 = net.addAccessPoint('ap1', cls=OVSKernelAP, ssid='ap1-ssid',
                             channel='36', mode='n', position='274.0,183.0,0')

    info( '*** Add hosts/stations\n')
    sta1 = net.addStation('sta1', ip='192.168.1.100/24',
                           position='188.0,144.0,0', channel = '36', mode = 'n')
    sta2 = net.addStation('sta2', ip='192.168.1.101/24',
                           position='200.0,221.0,0', channel = '36', mode = 'n')
 

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=1)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info( '*** Add links\n')

    net.plotGraph(max_x=1000, max_y=1000)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap1').start([c0])

    info( '*** Post configure nodes\n')
    sta1.setAssociation(ap1, intf='sta1-wlan0')
    sta2.setAssociation(ap1, intf='sta2-wlan0')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()


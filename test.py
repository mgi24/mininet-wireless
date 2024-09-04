from mn_wifi.link import wmediumd
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mininet.node import Controller,  Host,  OVSKernelSwitch

def topology():
    net = Mininet_wifi()
    s1  = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    h1 = net.addHost('h1', ip = '192.168.1.125/24')
    h2 = net.addHost('h2', ip = '192.168.1.130/24')
    c0 = net.addController('c0')
    net.configureWifiNodes()
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.build()
    s1.start([c0])

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()
from mininet.net import Mininet
from mininet.node import Host, OVSSwitch, Controller
from mininet.link import Intf
from mininet.log import setLogLevel, info
import time
from mn_wifi.cli import CLI
def myNetwork():
    net = Mininet(controller=Controller)
    
    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    
    info('*** Adding host\n')
    h1 = net.addHost('h1', ip='0.0.0.0')  # DHCP client configuration

    info('*** Creating links\n')
    net.addLink(h1, s1)

    info('*** Adding physical interface eth0 to switch\n')
    intf = Intf('eth0', node=s1)

    info('*** Starting network\n')
    net.start()
    CLI(net)
    info('*** Running DHCP client on host\n')
    h1.cmd('dhclient h1-eth0')
    
    info('*** Checking IP address\n')
    ip_result = h1.cmd('ifconfig h1-eth0')
    print(ip_result)

    info('*** Pinging 8.8.8.8 continuously with 1-second interval\n')

    # Running ping in a loop and displaying results
    try:
        while True:
            ping_result = h1.cmd('ping -c 1 8.8.8.8')
            ip_result = h1.cmd('ifconfig h1-eth0')
            print(f'Ping Result:\n{ping_result}\n')
            print(f'IP Configuration:\n{ip_result}\n')
            time.sleep(1)
    except KeyboardInterrupt:
        info('*** Stopping ping\n')
    
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

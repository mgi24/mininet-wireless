from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import OVSKernelAP
from mn_wifi.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def myNetwork():
    # Inisialisasi jaringan menggunakan Mininet_wifi
    net = Mininet_wifi(controller=Controller)

    info("*** Menambahkan controller\n")
    c0 = net.addController('c0')

    info("*** Menambahkan switch\n")
    s1 = net.addSwitch('s1')

    info("*** Menambahkan host\n")
    h1 = net.addHost('h1', ip='0.0.0.0')

    info("*** Menghubungkan switch ke interface fisik ens33\n")
    Intf('ens33', node=s1)
    
    info("*** Menghubungkan switch ke host\n")
    net.addLink(s1, h1)




    info("*** Menambahkan access point\n")
    ap1 = net.addAccessPoint('ap1', ssid="simplewifi", mode="g", channel="1")
    
    info("*** Menghubungkan switch ke access point\n")
    net.addLink(s1, ap1)

    
    

    

    info("*** Mengkonfigurasi jaringan\n")
    net.configureNodes()
    net.build()
    c0.start()
    s1.start([c0])
    ap1.start([c0])
    h1.cmd('dhclient h1-eth0')
    h1.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")


    info("*** Memulai CLI\n")
    CLI(net)

    info("*** Menghentikan jaringan\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

from mininet.net import Mininet
from mininet.node import Host, OVSSwitch, Controller
from mininet.link import Intf
from mininet.log import setLogLevel, info
import time
import json
def run_speedtest(host):
    # Menjalankan speedtest dan mengembalikan output JSON sebagai dictionary
    result = host.cmd('speedtest -s 13777 -p no --format=json')
    return json.loads(result)

def myNetwork():
    net = Mininet(controller=Controller)
    
    info('*** Adding controller\n')
    net.addController('c0')

    info('*** Adding switch\n')
    s1 = net.addSwitch('s1')
    
    info('*** Adding host\n')
    h1 = net.addHost('h1', ip='0.0.0.0')  # DHCP client configuration
    h2 = net.addHost('h2', ip='0.0.0.0')

    info('*** Creating links switch >===< host\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    
    info('*** Adding physical interface ens33 >===< switch\n')
    intf = Intf('ens33', node=s1)

    info('*** Starting network\n')
    net.start()

    info('*** Running DHCP client on host\n')
    h1.cmd('dhclient h1-eth0')
    h2.cmd('dhclient h2-eth0')

    info('*** Checking IP address host\n')
    
    print(f"IP 1:{h1.cmd('hostname -I')}")
    print(f"IP 2:{h2.cmd('hostname -I')}")
    
    info('*** Changing DNS server\n')
    h1.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
    #print(h1.cmd("nmcli dev show | grep 'IP4.DNS'") )
    h2.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
    #print(h2.cmd("nmcli dev show | grep 'IP4.DNS'") )

    info('*** Pinging google ')
    print(f"host 1{h1.cmd('ping -c 1 google.com')}")
    print(f"host 1{h2.cmd('ping -c 1 google.com')}")

    info('*** Speedtest server Indosat TBK \n')
    all_results = []
    for i in range(3):
        print(f"Running test {i+1} on h1...")
        result = run_speedtest(h1)
        all_results.append(result)
    with open('/tmp/speedtest_h1.json', 'w') as f:
        json.dump(all_results, f, indent=4)

    #time.sleep(30);
    print(h1.cmd ('cat /tmp/speedtest_h1.json'))
    print(h1.cmd ('cat /tmp/speedtest_h2.json'))
    # Running ping in a loop and displaying results


    info('*** Stopping network\n')
    net.stop()

#start mininet
if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

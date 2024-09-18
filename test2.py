#!/usr/bin/env python

'This example creates a simple network topology with 1 AP and 2 stations'

import sys
import pandas as pd
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller,  Host,  OVSKernelSwitch
from mininet.link import Intf
from random import uniform
import json
import time
import matplotlib.pyplot as plt
import os
from threading import Thread
def pinghost(net, host1, host2):
    h1 = net.get(host1)
    h2 = net.get(host2)

    if h1 and h2:
        h1_ip_output = h1.cmd('hostname -I')
        h1_ip_list = h1_ip_output.split()
        h2_ip_output = h2.cmd('hostname -I')
        h2_ip_list = h2_ip_output.split()
        
        if h1_ip_list and h2_ip_list:
            h1_ip = [ip for ip in h1_ip_list if ':' not in ip][0]
            h2_ip = [ip for ip in h2_ip_list if ':' not in ip][0]
            result = h1.cmd(f'ping -c 4 {h2_ip}')
        else:
            print("Failed to retrieve IP for h1 or h2")
        print(result)
        print(f"Host {host1} or {host2} not found")
                   
def run_speedtest(sta, server_port,server_name, results, index):
    # Run the speedtest command and capture the output
    result = sta.cmd(f"speedtest -s {server_port} --format=json")
    print(f"test {sta.name} server {server_port} {server_name} done")
    
    try:
        result_json = json.loads(result)
        results[index] = result_json
    except json.JSONDecodeError as e:
        print(result)
        try:
            result = '{' + '"type":"result"' + result.split('"type":"result"')[-1]
            result_json = json.loads(result)
            
            results[index] = result_json
        except:
            try:
                result = '{"' + "error" + result.split('error')[-1]
                result_json = json.loads(result)
            
                results[index] = result_json
            except:
                print(result)
                print(f"Error decoding JSON for {sta.name}: {e}")

class CustomCLI(CLI):
    def do_pinghost(self, line):
        "Ping test: pinghost <host1> <host2>"
        args = line.split()
        if len(args) != 2:
            print("Usage: pinghost <host1> <host2>")
            return
        host1 = args[0]
        host2 = args[1]
        pinghost(self.mn, host1, host2)

    def do_checkarg(self, line):
        "Check the number of arguments provided"
        args = line.split()
        num_args = len(args)
        print(f"Number of arguments provided: {num_args}")
        if num_args == 0:
            print("No arg")
        else:
            for arg in args:
                print(arg)

    


    def do_speedtest(self, line):
        sta_list = self.mn.stations
        args = line.split()
        num_args = len(args)
        if num_args > 0:
            for arg in args:
                print("removing previous run json...")
                sta_list[0].cmd('cd /home/mamad/Documents/mininetlab/result && rm -f speedtest*')

                print("starting speedtest...")
                sta = self.mn.get(arg)
                if sta:
                    sta.cmd(f"speedtest -s 13777 --format json > /home/mamad/Documents/mininetlab/result/speedtest{sta.name}.json")
                    print(f"result for {sta.name}")
                    result_file = f'speedtest{sta.name}.json'
                    with open(result_file) as f:
                        data = json.load(f)
                        data['download']['bandwidth'] *= 8
                        data['upload']['bandwidth'] *= 8
                        data_str = json.dumps(data, indent=4)
                        print(f"Speedtest result on {sta.name}:")
                        print(data_str)
                        print(f"Upload Speed : {data['upload']['bandwidth']/1000000} Mbps")
                        print(f"Download Speed : {data['download']['bandwidth']/1000000} Mbps")

                else:
                    print(f"Host {arg} not found")

                


        else:
            "Run speedtest on all STAs"
            results = [None] * len(sta_list)
            threads = []
            if sta_list:
                print("removing previous run json...")
                sta_list[0].cmd('cd /home/mamad/Documents/mininetlab/result && rm -f *')
                print("starting speedtest...")

                for i, sta in enumerate(sta_list):
                    if i % 4 == 0:
                        server_port = 41848  # Global Media Data Prima
                        server_name = "Global Media Data Prima"
                    elif i % 4 == 1:
                        server_port = 13825  # GMEDIA
                        server_name = "GMEDIA" 
                    elif i % 4 == 2:
                        server_port = 33207  # Lintas Data Prima
                        server_name = "Lintas Data Prima"
                    elif i % 4 == 3:
                        server_port = 36813  # Citranet
                        server_name = "Citranet"
                    # Run speedtest in the background and capture the PID
                    print(f"Starting speedtest on {sta.name} with server port {server_port} {server_name}")
                    thread = Thread(target=run_speedtest, args=(sta, server_port, server_name, results, i))
                    threads.append(thread)
                    thread.start()
                    time.sleep(0.1)

                for thread in threads:
                    thread.join()
                print("All processes completed")

                print("Waiting remaning process...")
                time.sleep(1)

                for i, result in enumerate(results):

                    if i % 4 == 0:
                        server_port = 41848  # Global Media Data Prima
                        server_name = "Global Media Data Prima"
                    elif i % 4 == 1:
                        server_port = 13825  # GMEDIA
                        server_name = "GMEDIA" 
                    elif i % 4 == 2:
                        server_port = 33207  # Lintas Data Prima
                        server_name = "Lintas Data Prima"
                    elif i % 4 == 3:
                        server_port = 36813  # Citranet
                        server_name = "Citranet"
                    print(f"Result on sta{i+1} server {server_name}")
                    if result:
                        try:
                            data = json.loads(json.dumps(result))
                            result_file = f'/home/mamad/Documents/mininetlab/result/sta{i+1}.json'
                            data['rssi'] = sta_list[i].wintfs[0].rssi
                            if 'error' in data:
                                data = {'error':data['error'],
                                        'server':{'name': server_name}, 'rssi':sta_list[i].wintfs[0].rssi}
                            with open(result_file, 'w') as f:
                                json.dump(data, f, indent=4)
                            print(f"Result saved to {result_file}")

                            
                        except json.JSONDecodeError as e:
                            print(f"Failed to decode JSON: {e}")
                    else:
                        print("No result available")
                        result_file = f'/home/mamad/Documents/mininetlab/result/sta{i+1}.json'
                        with open(result_file, 'w') as f:
                            json.dump({'error':'SPEEDTEST ERROR', 'server':{'name': server_name},'rssi':sta_list[i].wintfs[0].rssi}, f, indent=4)
                        
            else:
                print("No STAs found")
        

    def do_stalist(self, line):
        "Print all available STAs"
        sta_list = self.mn.stations
        if sta_list:
            for sta in sta_list:
                ip_output = sta.cmd('hostname -I')
                ip_list = ip_output.split()
                ipv4_list = [ip for ip in ip_list if ':' not in ip]
                if ipv4_list:
                    print(f"IP {sta.name}: {ipv4_list[0]}")
                else:
                    print(f"Failed to retrieve IPv4 for {sta.name}")
        else:
            print("No STAs found")
   

    def do_bandwidth(self, line):
        "Run bandwidth test between two STAs"
        args = line.split()
        if len(args) != 2:
            print("Usage: bandwidth <sta1> <sta2>")
            return
        sta1 = args[0]
        sta2 = args[1]

        sta1 = self.mn.get(sta1)
        sta2 = self.mn.get(sta2)

        if sta1 and sta2:
            h1_ip_output = sta1.cmd('hostname -I')
            h1_ip_list = h1_ip_output.split()
            h2_ip_output = sta2.cmd('hostname -I')
            h2_ip_list = h2_ip_output.split()

            if h1_ip_list and h2_ip_list:
                h1_ipv4 = [ip for ip in h1_ip_list if ':' not in ip][0]
                h2_ipv4 = [ip for ip in h2_ip_list if ':' not in ip][0]
                sta1.cmd('iperf -s &')
                print(f"Upload test from {sta1.name} to {sta2.name}")
                print(sta2.cmd(f'iperf -c {h1_ipv4} -t 10 -i 1 -R'))
                print(f"Download test from {sta2.name} to {sta1.name}")
                print(sta2.cmd(f'iperf -c {h1_ipv4} -t 10 -i 1'))
            else:
                print("Failed to retrieve IPv4 for h1 or h2")
        else:
            print(f"Host {sta1} or {sta2} not found")
        sta1.cmd('killall iperf')



    def do_dhcp(self, line):
        "Run DHCP client on all STAs"
        sta_list = self.mn.stations
        if sta_list:
            for sta in sta_list:
                sta.cmd(f"dhclient {sta.name}-wlan0")
                print(f"DHCP client started on {sta.name}")
                ip_output = sta.cmd('hostname -I')
                ip_list = ip_output.split()
                if ip_list:
                    print(f"IP {sta.name}: {ip_list[0]}")
                    time.sleep(0.1)
                else:
                    print(f"Failed to retrieve IP for {sta.name}")
            sta_list[0].cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
        else:
            print("No STAs found")
        
 
    
        
            
        
def generate_random_position(ap_position, radius):
    x_ap, y_ap, z_ap = ap_position
    # Generate random offset within the radius
    x_offset = uniform(-radius, radius)
    y_offset = uniform(-radius, radius)
    return (x_ap + x_offset, y_ap + y_offset, z_ap)


def topology():
    "Create a network."
    net = Mininet_wifi()

    info("*** Creating nodes\n")
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    
    
    info("*** Adding STAs\n")
    

    # Input jumlah sta dan ap
    sta_count = int(input("Masukkan jumlah sta: "))
    ap_count = int(input("Masukkan jumlah ap: "))

    # List untuk menyimpan daftar access point dan station
    aps = []
    stations = []

    # Buat access point sesuai dengan input
    for i in range(1, ap_count + 1):
        ap_name = f'ap{i}'

        aps.append(ap_name)  # Menambahkan nama AP ke dalam list aps


    # Buat station sesuai dengan input
    for i in range(1, sta_count + 1):
        sta_name = f'sta{i}'
        stations.append(sta_name)  # Menambahkan nama station ke dalam list stations

    # Bagikan sta ke ap secara merata
    sta_per_ap = sta_count // ap_count  # Pembagian sta per ap
    extra_sta = sta_count % ap_count     # Sisa sta yang perlu didistribusikan

    # Menyimpan pembagian sta ke setiap ap
    sta_distribution = {ap: [] for ap in aps}  # Dictionary untuk menyimpan distribusi

    sta_index = 0
    for ap in aps:
        # Tambahkan sta_per_ap ke setiap ap
        for _ in range(sta_per_ap):
            sta_distribution[ap].append(stations[sta_index])
            sta_index += 1

        # Jika ada sisa sta, tambahkan satu sta tambahan ke beberapa ap
        if extra_sta > 0:
            sta_distribution[ap].append(stations[sta_index])
            sta_index += 1
            extra_sta -= 1

    # Output hasil distribusi
    for ap, sta_list in sta_distribution.items():
        
        print(f"{ap} memiliki {len(sta_list)} sta: {', '.join(sta_list)}")

    aps = []
    for i in range(1, ap_count + 1):
        ap = net.addAccessPoint(f'ap{i}', ssid=f"wireless{i}", mode="n", channel="36", position=f'{200.0*i},50.0,0.0')
        aps.append(ap)




    radius = 3
    stations = []
    for i, (ap, sta_list) in enumerate(sta_distribution.items()):
        for sta_name in sta_list:
            ap_position = aps[i].position
            sta_position = generate_random_position(ap_position, radius)
            mac_address = f'02:00:00:00:{i:02x}:{len(stations):02x}'
            sta = net.addStation(sta_name, ip='0.0.0.0', position=sta_position, mode="n", channel="36", mac=mac_address)
            stations.append(sta)
            print(f"Added {sta_name} at position {sta_position} with MAC {mac_address}")
        

        
    
    info("*** Simulating Interference\n")
    net.setPropagationModel(model="logDistance", exp=3.0)

    h1 = net.addHost('h1', ip='0.0.0.0', mac='02:00:00:ff:ff:ff')
    h2 = net.addHost('h2', ip = '0.0.0.0')
    
    info("*** Adding controller\n")
    c0 = net.addController('c0')
    '''contollers = []
    for ap in aps:
        c = net.addController(f'c{ap}')
        contollers.append(c)'''

    info("*** Configuring nodes\n")
    net.configureNodes()

    info('*** Adding physical interface ens33 >===< switch\n')
    intf = Intf('ens37', node=s1)
    
    info("*** Connecting Stations to AP\n")
    for i,(ap, sta_list)  in enumerate(sta_distribution.items()):
        for sta_name in sta_list:
            ap=aps[i]
            sta = net.get(sta_name)
            sta.setAssociation(ap, intf=f'{sta_name}-wlan0')
            print(f"Connecting {sta.name} to {ap.name}")
    
    info("*** Wiring up switch\n")
    for ap in aps:
        net.addLink(s1, ap)
        print(f"Connecting {ap.name} to switch")
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    
    info("*** Plotting Graph\n")
    net.plotGraph( min_x=0, max_x=70,min_y = 0, max_y=80)
    
    info("*** Starting network\n")
    net.build()
    c0.start()
    '''for contoller in contollers:
        contoller.start()'''

    for i, ap in enumerate(aps):
        ap.start([c0])
        
    s1.start([c0])

    info("*** Checking RSSI\n")
    time.sleep(10)
    rssi = []
    for sta in stations:
        print(f"{sta.name} {sta.wintfs[0].rssi}")
        rssi.append(sta.wintfs[0].rssi)
    
            
    
    info("*** Getting IP's from DHCP\n")
    h1.cmd('dhclient h1-eth0')
    #h2.cmd('dhclient h2-eth0')
    
    
    #print(stations)

        
    print(f"IP h1:{h1.cmd('hostname -I')}")
    print(f"IP h2:{h2.cmd('hostname -I')}")
    
    info("*** Setting DNS up\n")
    h1.cmd("echo 'nameserver 192.168.1.1' > /etc/resolv.conf")
    
    info("*** Running Custom CLI\n")
    CustomCLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
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
            
            if sta_list:
                print("removing previous run json...")
                sta_list[0].cmd('cd /home/mamad/Documents/mininetlab/result && rm -f speedtest*')
                print("starting speedtest...")
                
                
                pids = []

                for i, sta in enumerate(sta_list):
        
                    if i % 4 == 0:
                        server_port = 13777
                    elif i % 4 == 1:
                        server_port = 13825
                    elif i % 4 == 2:
                        server_port = 33207
                    elif i % 4 == 3:
                        server_port = 36813
                    

                    output = sta.cmd(f"speedtest -s {server_port} --format json > /home/mamad/Documents/mininetlab/result/speedtest{sta.name}.json & echo $!")
                    
                    pid = output.strip()
                    time.sleep(0.1)
                    print(sta.name,pid)
                    pid = pid.split()[1]
                    print(sta.name,pid)
                    pids.append(pid)
                    
                    
                while(True):
                    if not pids:
                        break
                    for pid in pids:
                        check_pid = sta_list[0].cmd(f"ps -p {pid}")
                        if pid not in check_pid:
                            print(f"PID {pid} done testing")
                            pids.remove(pid)


                print("formating json to be more readable...")

                upload_speeds = []
                download_speeds = []
                excel_data = []
                sta_error = 0
                time.sleep(60)

                for sta in sta_list:
                    result_file = f'/home/mamad/Documents/mininetlab/result/speedtest{sta.name}.json'
                    with open(result_file) as f:
                        data = json.load(f)

                        if 'error' in data:
                            upload = 0
                            download = 0
                        else:
                            data['upload']['bandwidth'] *= 8
                            data['download']['bandwidth'] *= 8
                            upload = data['download']['bandwidth']
                            download = data['upload']['bandwidth']
        
                        upload_speeds.append(upload)
                        download_speeds.append(download)
                        data_str = json.dumps(data, indent=4)
                        print(f"Speedtest result on {sta.name}:")
                        print(data_str)
                        if 'error' in data:
                            sta_error+=1
                            excel_result = {
                                
                                "station": sta.name, 
                                "timestamp": "error",
                                "ping jitter": "error",
                                "ping latency": "error",
                                "ping low": "error",
                                "ping high": "error",
                                "download bandwidth": "error",
                                "download bytes": "error",
                                "download elapsed": "error",
                                "download latency iqm": "error",
                                "download latency low": "error",
                                "download latency high": "error",
                                "download latency jitter": "error",
                                "upload bandwidth": "error",
                                "upload bytes": "error",
                                "upload elapsed": "error",
                                "upload latency iqm": "error",
                                "upload latency low": "error",
                                "upload latency high": "error",
                                "upload latency jitter": "error",
                                "packet loss": "error",
                                "isp": "error",
                                "interface internal ip": "error",
                                "interface name": "error",
                                "interface mac": "error",
                                "interface is vpn": "error",
                                "interface external ip": "error",
                                "server id": "error",
                                "server host": "error",
                                "server port": "error",
                                "server name": "error",
                                "server location": "error",
                                "server country": "error",
                                "result id": "error",
                                "result url": "error",
                                "result persisted": "error",
                                "error_message": data['error']
                            }
                        else:

                            excel_result = {
                                
                                "station": sta.name,  
                                "timestamp": data.get('timestamp', 'error'),
                                "ping jitter": data['ping'].get('jitter', 'error'),
                                "ping latency": data['ping'].get('latency', 'error'),
                                "ping low": data['ping'].get('low', 'error'),
                                "ping high": data['ping'].get('high', 'error'),
                                "download bandwidth": data['download'].get('bandwidth', 'error'),
                                "download bytes": data['download'].get('bytes', 'error'),
                                "download elapsed": data['download'].get('elapsed', 'error'),
                                "download latency iqm": data['download']['latency'].get('iqm', 'error') if 'download' in data and 'latency' in data['download'] else 'error',
                                "download latency low": data['download']['latency'].get('low', 'error') if 'download' in data and 'latency' in data['download'] else 'error',
                                "download latency high": data['download']['latency'].get('high', 'error') if 'download' in data and 'latency' in data['download'] else 'error',
                                "download latency jitter": data['download']['latency'].get('jitter', 'error') if 'download' in data and 'latency' in data['download'] else 'error',
                                "upload bandwidth": data['upload'].get('bandwidth', 'error'),
                                "upload bytes": data['upload'].get('bytes', 'error'),
                                "upload elapsed": data['upload'].get('elapsed', 'error'),
                                "upload latency iqm": data['upload']['latency'].get('iqm', 'error') if 'upload' in data and 'latency' in data['upload'] else 'error',
                                "upload latency low": data['upload']['latency'].get('low', 'error') if 'upload' in data and 'latency' in data['upload'] else 'error',
                                "upload latency high": data['upload']['latency'].get('high', 'error') if 'upload' in data and 'latency' in data['upload'] else 'error',
                                "upload latency jitter": data['upload']['latency'].get('jitter', 'error') if 'upload' in data and 'latency' in data['upload'] else 'error',
                                "packet loss": data.get('packetLoss', 'error'),
                                "isp": data.get('isp', 'error'),
                                "interface internal ip": data['interface'].get('internalIp', 'error') if 'interface' in data else 'error',
                                "interface name": data['interface'].get('name', 'error') if 'interface' in data else 'error',
                                "interface mac": data['interface'].get('macAddr', 'error') if 'interface' in data else 'error',
                                "interface is vpn": data['interface'].get('isVpn', 'error') if 'interface' in data else 'error',
                                "interface external ip": data['interface'].get('externalIp', 'error') if 'interface' in data else 'error',
                                "server id": data['server'].get('id', 'error'),
                                "server host": data['server'].get('host', 'error'),
                                "server port": data['server'].get('port', 'error'),
                                "server name": data['server'].get('name', 'error'),
                                "server location": data['server'].get('location', 'error'),
                                "server country": data['server'].get('country', 'error'),
                                "result id": data['result'].get('id', 'error'),
                                "result url": data['result'].get('url', 'error'),
                                "result persisted": data['result'].get('persisted', 'error'),
                                "error_message": "No error"
                            }
                            
                            if 'latency' not in data['upload']:
                                excel_result['upload latency iqm'] = "error"
                                excel_result['upload latency low'] = "error"
                                excel_result['upload latency high'] = "error"
                                excel_result['upload latency jitter'] = "error"
                            else:
                                excel_result['upload latency iqm'] = data['upload']['latency']['iqm']
                                excel_result['upload latency low'] = data['upload']['latency']['low']
                                excel_result['upload latency high'] = data['upload']['latency']['high']
                                excel_result['upload latency jitter'] = data['upload']['latency']['jitter']
                           
                        excel_data.append(excel_result)
                # Create a pandas dataframe
                excel_result["total failed"] = sta_error
                df = pd.DataFrame(excel_data)
                # Save to excel
                output_file = "/home/mamad/Documents/mininetlab/result/speedtest_helmi.xlsx"
                df.to_excel(output_file, index=False)

                total_upload_speed = sum(upload_speeds)
                total_download_speed = sum(download_speeds)
                print(f"Total upload speed: {total_upload_speed}")
                print(f"Total download speed: {total_download_speed}")
                

                upload_speeds_mbps = [speed / 1000000 for speed in upload_speeds]
                download_speeds_mbps = [speed / 1000000 for speed in download_speeds]
                total_upload_speed_mbps = total_upload_speed / 1000000
                total_download_speed_mbps = total_download_speed / 1000000

                plt.figure()
                plt.plot(upload_speeds_mbps, label='Upload Speed')
                plt.plot(download_speeds_mbps, label='Download Speed')
                plt.axhline(y=total_upload_speed_mbps, color='r', linestyle='--', label='Total Upload Speed')
                plt.axhline(y=total_download_speed_mbps, color='g', linestyle='--', label='Total Download Speed')
                plt.xlabel('Station')
                plt.ylabel('Speed (Mbps)')
                plt.title('Upload and Download Speeds')
                plt.legend()
                plt.show()

                
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
    ap1 = net.addAccessPoint('ap1', ssid="simpletopo", mode="n",
                             channel="36", position='50.0,50.0,0.0')
    
    info("*** Adding STAs\n")
    ap_position = (50, 50, 0)
    sta_count = int(input("Enter the number of stations to add: "))
    radius = 3
    stations = []
    for i in range (sta_count):
        sta_name = f'sta{i+1}'
        sta_position = generate_random_position(ap_position, radius)
        sta = net.addStation(sta_name,ip='0.0.0.0' ,position=sta_position, mode = "n", channel = "36")
        stations.append(sta)
        print(f"Added {sta_name} at position {sta_position}")
    
    info("*** Simulating Interference\n")
    net.setPropagationModel(model="logDistance", exp=2.0)

    h1 = net.addHost('h1', ip = '0.0.0.0')
    h2 = net.addHost('h2', ip = '0.0.0.0')
    
    c0 = net.addController('c0')

    info("*** Configuring nodes\n")
    net.configureNodes()

    info('*** Adding physical interface ens33 >===< switch\n')
    intf = Intf('ens33', node=s1)
    
    info("*** Connecting Stations to AP\n")
    for i, sta in enumerate(stations):
        sta.setAssociation(ap1, intf=f'{sta.name}-wlan0')
    
    info("*** Wiring up switch\n")
    net.addLink(s1, ap1)
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    
    info("*** Plotting Graph\n")
    #net.plotGraph( min_x=0, max_x=70,min_y = 0, max_y=80)
    
    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    s1.start([c0])

    info("*** Getting IP's from DHCP\n")
    h1.cmd('dhclient h1-eth0')
    h2.cmd('dhclient h2-eth0')
    print(stations)
    for i, sta in enumerate(stations):
        sta.cmd(f'dhclient {sta.name}-wlan0')
        ip_output = sta.cmd('hostname -I')
        ip_list = ip_output.split()
        if ip_list:
            print(f"IP {sta.name}: {ip_list[0]}")
        else:
            print(f"Failed to retrieve IP for {sta.name}")
        
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
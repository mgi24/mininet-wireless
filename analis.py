import json
import pandas as pd
import os
import matplotlib.pyplot as plt

def read_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                json_files.append(os.path.join(root, file))
    
    sta_error = 0
    upload_speeds = []
    download_speeds = []
    excel_data = []
    json_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0][3:]))
    for file in json_files:
        with open(file) as f:
            sta_name = os.path.splitext(os.path.basename(file))[0]
            print(f"Checking {f}")
            data=[]
            #data = json.load(f)
            if os.path.getsize(file) > 0:
                data = json.load(f)
                data_str = json.dumps(data, indent=4)
                #print(data_str)
                if 'error' in data:
                    upload = 0
                    download = 0
                    sta_error+=1
                    excel_result = {
                        
                        "station": sta_name, 
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
                        "server name": data['server']['name'],
                        "server location": "error",
                        "server country": "error",
                        "result id": "error",
                        "result url": "error",
                        "result persisted": "error",
                        "error_message": data['error']
                    }
                else:
                    data['download']['bandwidth'] *= 8
                    data['upload']['bandwidth'] *= 8
                    download = data['download']['bandwidth']
                    upload = data['upload']['bandwidth']
                    excel_result = {
                                    
                        "station": sta_name,  
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
                    
                upload_speeds.append(upload)
                download_speeds.append(download)


                excel_data.append(excel_result)
            else:
                print(f"Empty JSON file: {sta_name}")
                excel_result = {
                        
                        "station": sta_name, 
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
                        "error_message": "SPEEDTEST TASK FAILED"
                    }
                excel_data.append(excel_result)
    excel_result["total failed"]=sta_error
    df = pd.DataFrame(excel_data)
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
read_json_files("/home/mamad/Documents/mininetlab/result")

            
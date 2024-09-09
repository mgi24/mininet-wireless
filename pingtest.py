import sys

def ping_host(net, hostname, target='google.com'):
    host = net.get(hostname)
    print(f"Pinging {target} from {hostname}...")
    result = host.cmd(f'ping -c 4 {target}')
    print(result)

# In Mininet-WiFi CLI, 'net' is an object of Mininet class that contains the network topology
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py testping.py <hostname>")
    else:
        hostname = sys.argv[1]
        ping_host(net, hostname)

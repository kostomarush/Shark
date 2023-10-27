import nmap

# Создайте объект nmap.PortScanner()
nm = nmap.PortScanner()
# Выполните сканирование UDP-портов
closed_ports = 0
result = nm.scan(hosts='127.0.0.1', arguments='-sT')
a = 0
b = 1000
host_info = {}
for host, scan_result in result['scan'].items():
    host_info[host] = {}
    host_info[host]['host'] = host
    host_info[host]['state'] = nm[host].state()
    host_info[host]['open_ports'] = []
    if 'tcp' in nm[host]:
        for port, info in scan_result['tcp'].items():
            port_data = {
                'port': port,
                'reason': info['reason'],
                'service': info['name']
            }
            host_info[host]['open_ports'].append(port_data)
    else:
        host_info[host]['open_ports'] = 'down'
        print("No open TCP ports found.")

for host, info in host_info.items():
    host=info['host']
    state_scan=info['state']
    print(host)
    print(state_scan)
    for port_info in info['open_ports']:
        port = port_info['port']
        reason = port_info['reason']
        service = port_info['service']


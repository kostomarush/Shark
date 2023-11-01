import nmap


host_info = {}
nm = nmap.PortScanner()
host = '127.0.0.1'
cve_report = 'True'
result = nm.scan(host, arguments=f'-sS -p{ports}', sudo=True)
if result['scan']:
    host_info['host'] = host
    host_info['state'] = nm[host].state()
    host_info['ports'] = []
    if 'tcp' in nm[host]:
        for port, info in nm[host]['tcp'].items():
            if cve_report == 'True':
                cve_information = cve_info(host, port)
            else:
                cve_information = 'Empty'
            port_data = {
                        'port': f'{port}',
                        'reason': info['reason'],
                        'service': info['name'],
                        'cve': cve_information
                        }
            host_info['ports'].append(port_data)
    else:
        host_info['ports'] = 'down'
        print("No open TCP ports found.")
else:
    print('hosts is down')

print(host_info)
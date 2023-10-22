import nmap

# Создайте объект nmap.PortScanner()
nm = nmap.PortScanner()
# Выполните сканирование UDP-портов
closed_ports = 0
result = nm.scan(hosts='127.0.0.0/30', arguments='-O')
a = 0
b = 1000
host_info = {}
for host, scan_result in result['scan'].items():
    host_info[host] = {}
    host_info[host]['host'] = host
    host_info[host]['state'] = nm[host].state()
    
    # Проверка наличия информации об операционной системе
    if 'osmatch' in scan_result and isinstance(scan_result['osmatch'], list) and len(scan_result['osmatch']) > 0:
        osmatch = scan_result['osmatch'][0]
        name = osmatch['name']
        host_info[host][name] = {}

        # Проверка наличия информации о производителе
        if 'osclass' in osmatch and isinstance(osmatch['osclass'], list) and len(osmatch['osclass']) > 0:
            osclass = osmatch['osclass'][0]
            host_info[host][name]['vendor'] = osclass.get('vendor', 'N/A')
            host_info[host][name]['osfamily'] = osclass.get('osfamily', 'N/A')
            host_info[host][name]['osgen'] = osclass.get('osgen', 'N/A')
            host_info[host][name]['accuracy'] = osclass.get('accuracy', 'N/A')
        else:
            host_info[host][name] = {
                'vendor': 'N/A',
                'osfamily': 'N/A',
                'accuracy': 'N/A',
                'osgen': 'N/A'
            }
    else:
        host_info[host][name] = {
            'vendor': 'N/A',
            'osfamily': 'N/A',
            'accuracy': 'N/A',
            'osgen': 'N/A'
        }

print(host_info)

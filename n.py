import nmap

# Создайте объект nmap.PortScanner()
nm = nmap.PortScanner()
# Выполните сканирование UDP-портов
result = nm.scan(hosts='127.0.0.1', arguments='-sS')

for host, scan_result in result['scan'].items():
    print(f"Host: {host}")

    for ports, info in scan_result['tcp'].items():
        print(f"Port: {ports}")
        state = info['state']
        reason = info['reason']
        service = info['name']

        print(f"State: {state}")
        print(f"Reason: {reason}")
        print(f"Service: {service}")


import nmap

# Создаем объект класса PortScanner
nm = nmap.PortScanner()

# Список IP-адресов, которые вы хотите отсканировать
ip_addresses = ['10.33.102.39', '10.33.102.40', '10.33.102.41']

# Проходим по списку IP-адресов и сканируем каждый
for ip in ip_addresses:
    print(f"Scanning {ip}...")
    nm.scan(ip, arguments='-v -sV --script vulscan/ --script-args vulscandb=cve.csv')  # Замените аргументы на необходимые

    # Обработка результатов сканирования
    for host in nm.all_hosts():
        print(f"Host: {host}")
        print(f"State: {nm[host].state()}")
        print(f"Open Ports: {list(nm[host]['tcp'].keys())}")

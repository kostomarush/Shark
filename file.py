
import nmap

# Создаем объект класса PortScanner
nm = nmap.PortScanner()

# Список IP-адресов, которые вы хотите отсканировать
ip_addresses = '10.33.102.39/28'
# Проходим по списку IP-адресов и сканируем каждый
print(f"Scanning {ip_addresses}...")
nm.scan(ip_addresses, arguments='-v -sV')  # Замените аргументы на необходимые
# Обработка результатов сканирования
for host in nm.all_hosts():
    print(f"Host: {host}")
    print(f"State: {nm[host].state()}")
    if 'tcp' in nm[host]:
        open_ports = list(nm[host]['tcp'].keys())
        print(f"Open Ports: {open_ports}")
    else:
        print("No open TCP ports found.")

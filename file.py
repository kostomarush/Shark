
import nmap

# Создаем объект класса PortScanner
nm = nmap.PortScanner()

# Список IP-адресов, которые вы хотите отсканировать
ip_addresses = '10.33.101.48/28'
# Проходим по списку IP-адресов и сканируем каждый
print(f"Scanning {ip_addresses}...")
nm.scan(ip_addresses, arguments='-v -sV')  # Замените аргументы на необходимые
# Обработка результатов сканирования

host_info = {}
for host in nm.all_hosts():
    host_info[host] = {} 
    host_info[host]['host'] = host
    host_info[host]['state'] = nm[host].state()
    if 'tcp' in nm[host]:
        host_info[host]['open_ports'] = list(nm[host]['tcp'].keys())
    else:
        host_info[host]['open_ports'] = 'down'
        print("No open TCP ports found.")

print(host_info)
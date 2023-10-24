import nmap

ip_address = '127.0.0.1'
# SYN ACK Scan:
nm = nmap.PortScanner()
nm.scan(ip_address, arguments='-sV -p22 --script vulscan/ --script-args vulscandb=update_cve.csv')

ip_status = nm[ip_address].state()
protocols = nm[ip_address].all_protocols()[0]
open_ports = nm[ip_address]['tcp'].keys()
for ports in open_ports:
    script = nm[ip_address]['tcp'][ports].get('script', '')
    if script != '':
        all_chunk = script.get('vulscan', '')
    else:
        all_chunk = 'No'
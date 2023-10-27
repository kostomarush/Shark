import nmap

host = '127.0.0.1'
host_info = {}
port = 22
nm = nmap.PortScanner()
result = nm.scan(host, ports=f'{port}', arguments='-sV --script vulscan/ --script-args vulscandb=update_cve.csv')
if result['scan']:
    a = result['scan'][host]['tcp'][port]['script']['vulscan']

print (a)
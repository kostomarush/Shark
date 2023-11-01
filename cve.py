import nmap

host = '127.0.0.1'
host_info = {}
port = 8000
nm = nmap.PortScanner()
result = nm.scan(host, ports=f'{port}', arguments='-sV --script vulscan/ --script-args vulscandb=update_cve.csv')
cve_inf = result['scan'][host]['tcp'][port]['script']
if cve_inf:
    all_chunk = cve_inf.get('vulscan', 'Empty'),
else:
    all_chunk = 'No'

print (all_chunk)
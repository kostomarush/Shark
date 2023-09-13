
import nmap
ip = '127.0.0.1'
nm = nmap.PortScanner()
nm.scan(ip,'22', '-sV --script vulscan/ --script-args vulscandb=cve.csv')

open_ports = nm[ip]['tcp'].keys()
for ports in open_ports:
    print(f'Port:{ports}')
    script = nm[ip]['tcp'][ports].get('script','')
    if script!='':
        print(script.get('vulscan',''))
    else:
        print(nm[ip]['tcp'][ports]['state'])



import nmap

host = '127.0.0.0/30'
host_info = {}
nm = nmap.PortScanner()
result = nm.scan(host, arguments='-sV --script vulscan/ --script-args vulscandb=update_cve.csv')
if result['scan']:
    for ipadd, scan_result in result['scan'].items():
        host_info[ipadd] = {}
        host_info[ipadd]['host'] = ipadd
        host_info[ipadd]['cve_ports'] = []
        for port, info in scan_result['tcp'].items():
            script = info['script']
            if script:
                all_chunk = {
                            'port': f'{port}',
                            'cve': script.get('vulscan', ''),
                        }
                host_info[ipadd]['cve_ports'].append(all_chunk)
            else:
                all_chunk = 'No'
else:
    print('hosts is down')

print (host_info)
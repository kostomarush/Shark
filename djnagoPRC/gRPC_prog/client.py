import grpc
import prot_pb2, prot_pb2_grpc
import nmap


def scan():
    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    response = stub.scan(prot_pb2.DataClient(message = '7'))
    nm = nmap.PortScanner()
    ip_address = response.ip
    port = response.port
    #SYN ACK Scan:
    if response.mode == 'SYN':
        nm.scan(ip_address,port, '-v -sS', sudo=True)
        ip_status = nm[ip_address].state()
        protocols = nm[ip_address].all_protocols()[0]
        open_ports = nm[ip_address]['tcp'].keys()
        for ports in open_ports:
            state = nm[ip_address]['tcp'][ports]['state']
            stub.scan(prot_pb2.DataClient(ip_status=ip_status, protocols=protocols,open_ports=f'{ports}', state = nm[ip_address]['tcp'][ports]['state']))
            
    #UDP Scan
    if response.mode == 'UDP':
        nm.scan(ip_address, port, '-v -sU', sudo=True)
        ip_status = nm[ip_address].state()
        protocols = nm[ip_address].all_protocols()
        open_ports = nm[ip_address]['udp'].keys()
        for ports in open_ports:
            stub.scan(prot_pb2.DataClient(ip_status=ip_status, protocols=protocols,open_ports=f'{ports}',state = nm[ip_address]['udp'][ports]['state']))

    #Comprehensive Scan
    if response.mode == 'CS':
        nm.scan(ip_address, port, '-v -sS -sV -sC -A -O', sudo=True)
        ip_status = nm[ip_address].state()
        protocols = nm[ip_address].all_protocols()
        open_ports = nm[ip_address]['tcp'].keys()
        for ports in open_ports:
            stub.scan(prot_pb2.DataClient(ip_status=ip_status, protocols=protocols,open_ports=f'{ports}'), state = nm[ip_address]['tcp'][ports]['state'])
        

    #OS Detection
    if response.mode == 'OS':
        os_detection = nm.scan(ip_address, arguments="-O", sudo=True)['scan'][ip_address]['osmatch']
        vendor = os_detection[0]['osclass'][0]['vendor']
        os_family = os_detection[0]['osclass'][0]['osfamily']
        osgen = os_detection[0]['osclass'][0]['osgen']
        stub.scan(prot_pb2.DataClient(vendor=vendor, os_family=os_family, osgen=osgen))


if __name__ == "__main__":
    scan()
        
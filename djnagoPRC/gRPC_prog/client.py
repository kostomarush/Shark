import grpc
import prot_pb2, prot_pb2_grpc
import nmap


def scan():
    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    response = stub.scan(prot_pb2.DataClient(message = 'Hello'))
    nm = nmap.PortScanner()
    nm.scan(f'{response.ip}', f'{response.port}')
    print(nm['127.0.0.1']['tcp'].keys())
    stub.scan(prot_pb2.DataClient(scan_info = 'scanning'))

if __name__ == "__main__":
    scan()
        
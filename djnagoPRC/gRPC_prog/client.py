import grpc
import prot_pb2, prot_pb2_grpc
import nmap


def scan():
    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    response = stub.scan(prot_pb2.DataClient(message = 'Hello'))
    nm = nmap.PortScanner()
    scanning = nm.scan(f'{response.ip}', f'{response.port}')
    stub.scan(prot_pb2.DataClient(info_scan = scanning))

if __name__ == "__main__":
    scan()
        
import grpc
import prot_pb2, prot_pb2_grpc
import nmap
import time


def scan():
    for i in range(100):
        channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
        stub = prot_pb2_grpc.RPCStub(channel)
        response = stub.scan(prot_pb2.DataClient(state = 'Client_1 connect'))
        ip = response.ip
        port = response.port
        print(time.time())
        #nm = nmap.PortScanner()
        #nm.scan(f'{response.ip}', f'{response.port}')
        #state = nm[f'{response.ip}'].state()
        hi = stub.scan(prot_pb2.DataClient(state = 'up'))


if __name__ == "__main__":
    scan()
        
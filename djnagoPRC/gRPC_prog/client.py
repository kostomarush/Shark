import grpc
import prot_pb2, prot_pb2_grpc
import nmap
import time


def scan():
    channel = grpc.insecure_channel('localhost:50051', options=(('grpc.enable_http_proxy', 0),))
    stub = prot_pb2_grpc.RPCStub(channel)
    response = stub.scan(prot_pb2.DataClient(state = 'Client_1 connect'))
    ip = response.ip
    port = response.port
    nm = nmap.PortScanner()
    nm.scan(f'{response.ip}', f'{response.port}')
    state = nm[f'{response.ip}'].state()
    hostname = nm[f'{response.ip}'].hostname()
    protocols = nm[f'{response.ip}'].all_protocols()
    ports = nm[f'{response.ip}']['tcp'].keys()
    hi = stub.scan(prot_pb2.DataClient(state = 'up'))


if __name__ == "__main__":
    scan()
        
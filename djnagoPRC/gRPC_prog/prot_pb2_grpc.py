# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import prot_pb2 as prot__pb2


class RPCStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.scan = channel.unary_unary(
                '/RPC/scan',
                request_serializer=prot__pb2.DataClient.SerializeToString,
                response_deserializer=prot__pb2.DataServer.FromString,
                )
        self.segment_scan = channel.unary_unary(
                '/RPC/segment_scan',
                request_serializer=prot__pb2.DataClientSegment.SerializeToString,
                response_deserializer=prot__pb2.DataSegment.FromString,
                )
        self.SayHello = channel.unary_unary(
                '/RPC/SayHello',
                request_serializer=prot__pb2.HelloRequest.SerializeToString,
                response_deserializer=prot__pb2.HelloReply.FromString,
                )


class RPCServicer(object):
    """Missing associated documentation comment in .proto file."""

    def scan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def segment_scan(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SayHello(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RPCServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'scan': grpc.unary_unary_rpc_method_handler(
                    servicer.scan,
                    request_deserializer=prot__pb2.DataClient.FromString,
                    response_serializer=prot__pb2.DataServer.SerializeToString,
            ),
            'segment_scan': grpc.unary_unary_rpc_method_handler(
                    servicer.segment_scan,
                    request_deserializer=prot__pb2.DataClientSegment.FromString,
                    response_serializer=prot__pb2.DataSegment.SerializeToString,
            ),
            'SayHello': grpc.unary_unary_rpc_method_handler(
                    servicer.SayHello,
                    request_deserializer=prot__pb2.HelloRequest.FromString,
                    response_serializer=prot__pb2.HelloReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RPC', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RPC(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def scan(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RPC/scan',
            prot__pb2.DataClient.SerializeToString,
            prot__pb2.DataServer.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def segment_scan(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RPC/segment_scan',
            prot__pb2.DataClientSegment.SerializeToString,
            prot__pb2.DataSegment.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SayHello(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RPC/SayHello',
            prot__pb2.HelloRequest.SerializeToString,
            prot__pb2.HelloReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

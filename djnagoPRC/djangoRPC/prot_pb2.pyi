from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DataServer(_message.Message):
    __slots__ = ["ip", "port", "mode"]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ip: str
    port: str
    mode: str
    def __init__(self, ip: _Optional[str] = ..., port: _Optional[str] = ..., mode: _Optional[str] = ...) -> None: ...

class DataClient(_message.Message):
    __slots__ = ["message", "ip_status", "protocols", "open_ports", "state", "id_client"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IP_STATUS_FIELD_NUMBER: _ClassVar[int]
    PROTOCOLS_FIELD_NUMBER: _ClassVar[int]
    OPEN_PORTS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ID_CLIENT_FIELD_NUMBER: _ClassVar[int]
    message: str
    ip_status: str
    protocols: str
    open_ports: str
    state: str
    id_client: str
    def __init__(self, message: _Optional[str] = ..., ip_status: _Optional[str] = ..., protocols: _Optional[str] = ..., open_ports: _Optional[str] = ..., state: _Optional[str] = ..., id_client: _Optional[str] = ...) -> None: ...

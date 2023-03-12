from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DataClient(_message.Message):
    __slots__ = ["id_client", "ip_status", "message", "open_ports", "os_family", "osgen", "protocols", "state", "vendor"]
    ID_CLIENT_FIELD_NUMBER: _ClassVar[int]
    IP_STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OPEN_PORTS_FIELD_NUMBER: _ClassVar[int]
    OSGEN_FIELD_NUMBER: _ClassVar[int]
    OS_FAMILY_FIELD_NUMBER: _ClassVar[int]
    PROTOCOLS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    VENDOR_FIELD_NUMBER: _ClassVar[int]
    id_client: str
    ip_status: str
    message: str
    open_ports: str
    os_family: str
    osgen: str
    protocols: str
    state: str
    vendor: str
    def __init__(self, message: _Optional[str] = ..., ip_status: _Optional[str] = ..., protocols: _Optional[str] = ..., open_ports: _Optional[str] = ..., state: _Optional[str] = ..., vendor: _Optional[str] = ..., os_family: _Optional[str] = ..., osgen: _Optional[str] = ..., id_client: _Optional[str] = ...) -> None: ...

class DataServer(_message.Message):
    __slots__ = ["ip", "mode", "port"]
    IP_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    ip: str
    mode: str
    port: str
    def __init__(self, ip: _Optional[str] = ..., port: _Optional[str] = ..., mode: _Optional[str] = ...) -> None: ...

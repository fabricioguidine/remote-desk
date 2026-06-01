"""Protocol - message classes and serialization.

Control messages are JSON; frame payloads are binary. Both share a single
length-prefixed wire envelope so the transport layer can read one whole
message at a time from a byte stream. This module is pure and OS-agnostic.
"""
import json
import struct

# Message type constants (see docs/ARCHITECTURE.md).
REGISTER = "register"
AUTH = "auth"
SERVER_LIST = "server_list"
CONNECT = "connect"
FRAME = "frame"
INPUT = "input"
DISCONNECT = "disconnect"
ERROR = "error"

# Wire envelope: kind (1 byte) + payload length (4 bytes, big-endian) + payload.
KIND_JSON = 0
KIND_BINARY = 1
_HEADER = struct.Struct(">BI")
HEADER_SIZE = _HEADER.size


class ProtocolError(Exception):
    """Raised when bytes on the wire do not form a valid message."""


class Message:
    """A control message: a type plus arbitrary JSON-serializable fields."""

    def __init__(self, type, **fields):
        self.type = type
        self.fields = fields

    def to_dict(self):
        return {"type": self.type, **self.fields}

    @classmethod
    def from_dict(cls, data):
        if "type" not in data:
            raise ProtocolError("message missing 'type'")
        fields = {k: v for k, v in data.items() if k != "type"}
        return cls(data["type"], **fields)

    def __eq__(self, other):
        return (
            isinstance(other, Message)
            and self.type == other.type
            and self.fields == other.fields
        )

    def __repr__(self):
        return f"Message(type={self.type!r}, fields={self.fields!r})"


def encode_message(message):
    """Serialize a Message into a length-prefixed JSON envelope."""
    payload = json.dumps(message.to_dict()).encode("utf-8")
    return _HEADER.pack(KIND_JSON, len(payload)) + payload


def encode_frame(data):
    """Serialize raw binary frame bytes into a length-prefixed envelope."""
    if not isinstance(data, (bytes, bytearray)):
        raise ProtocolError("frame payload must be bytes")
    return _HEADER.pack(KIND_BINARY, len(data)) + bytes(data)


def decode(buffer):
    """Decode one envelope from the front of buffer.

    Returns (item, rest). item is a Message (JSON) or bytes (binary frame).
    If buffer does not yet hold a complete envelope, returns (None, buffer)
    so a streaming caller can read more and retry.
    """
    if len(buffer) < HEADER_SIZE:
        return None, buffer
    kind, length = _HEADER.unpack(buffer[:HEADER_SIZE])
    end = HEADER_SIZE + length
    if len(buffer) < end:
        return None, buffer
    payload = buffer[HEADER_SIZE:end]
    rest = buffer[end:]
    if kind == KIND_JSON:
        try:
            data = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ProtocolError(f"invalid JSON payload: {exc}") from exc
        return Message.from_dict(data), rest
    if kind == KIND_BINARY:
        return bytes(payload), rest
    raise ProtocolError(f"unknown message kind: {kind}")

"""Tests for the wire protocol: message and frame (de)serialization."""
import pytest

from desktop.common import protocol
from desktop.common.protocol import Message, ProtocolError


def test_message_round_trip():
    msg = Message(protocol.AUTH, token="secret", server_id="PC-1")
    item, rest = protocol.decode(protocol.encode_message(msg))
    assert item == msg
    assert item.type == protocol.AUTH
    assert item.fields == {"token": "secret", "server_id": "PC-1"}
    assert rest == b""


def test_message_to_from_dict():
    msg = Message(protocol.REGISTER, id="x")
    assert msg.to_dict() == {"type": "register", "id": "x"}
    assert Message.from_dict({"type": "register", "id": "x"}) == msg


def test_from_dict_without_type_raises():
    with pytest.raises(ProtocolError, match="missing 'type'"):
        Message.from_dict({"id": "x"})


def test_frame_round_trip():
    data = bytes(range(256)) * 4
    item, rest = protocol.decode(protocol.encode_frame(data))
    assert item == data
    assert isinstance(item, bytes)
    assert rest == b""


def test_encode_frame_rejects_non_bytes():
    with pytest.raises(ProtocolError, match="must be bytes"):
        protocol.encode_frame("not bytes")


def test_decode_incomplete_header_returns_none():
    item, rest = protocol.decode(b"\x00\x00")
    assert item is None
    assert rest == b"\x00\x00"


def test_decode_incomplete_payload_returns_none():
    wire = protocol.encode_message(Message(protocol.CONNECT, x=1))
    truncated = wire[:-1]
    item, rest = protocol.decode(truncated)
    assert item is None
    assert rest == truncated


def test_decode_leaves_trailing_bytes():
    a = protocol.encode_message(Message(protocol.CONNECT, n=1))
    b = protocol.encode_frame(b"\xde\xad")
    item, rest = protocol.decode(a + b)
    assert item == Message(protocol.CONNECT, n=1)
    assert rest == b


def test_decode_drains_mixed_stream_sequentially():
    stream = (
        protocol.encode_message(Message(protocol.REGISTER, id="s"))
        + protocol.encode_frame(b"frame-bytes")
        + protocol.encode_message(Message(protocol.DISCONNECT))
    )
    first, stream = protocol.decode(stream)
    second, stream = protocol.decode(stream)
    third, stream = protocol.decode(stream)
    assert first == Message(protocol.REGISTER, id="s")
    assert second == b"frame-bytes"
    assert third == Message(protocol.DISCONNECT)
    assert stream == b""


def test_decode_unknown_kind_raises():
    bad = b"\x09" + b"\x00\x00\x00\x00"  # kind=9, length=0
    with pytest.raises(ProtocolError, match="unknown message kind"):
        protocol.decode(bad)


def test_decode_invalid_json_raises():
    # kind=JSON, length=3, payload b'{' * 3 is not valid JSON
    import struct
    payload = b"{{{"
    bad = struct.pack(">BI", protocol.KIND_JSON, len(payload)) + payload
    with pytest.raises(ProtocolError, match="invalid JSON"):
        protocol.decode(bad)


def test_unicode_fields_round_trip():
    msg = Message(protocol.ERROR, detail="café — 你好 — naïve")
    item, _ = protocol.decode(protocol.encode_message(msg))
    assert item == msg

"""Tests for the framed Connection transport using an in-memory stub socket."""
import pytest

from desktop.common import protocol
from desktop.common.connection import Connection
from desktop.common.protocol import Message


class FakeSocket:
    """A loopback byte buffer exposing the sendall/recv surface Connection needs."""

    def __init__(self, incoming=b""):
        self.incoming = bytearray(incoming)
        self.sent = bytearray()
        self.closed = False

    def sendall(self, data):
        self.sent += data

    def recv(self, n):
        if not self.incoming:
            return b""
        chunk = bytes(self.incoming[:n])
        del self.incoming[:n]
        return chunk

    def close(self):
        self.closed = True


def test_send_message_writes_encoded_bytes():
    sock = FakeSocket()
    conn = Connection(sock)
    msg = Message(protocol.AUTH, token="t")
    conn.send_message(msg)
    assert bytes(sock.sent) == protocol.encode_message(msg)


def test_receive_message():
    msg = Message(protocol.REGISTER, id="srv")
    sock = FakeSocket(incoming=protocol.encode_message(msg))
    assert Connection(sock).receive() == msg


def test_receive_frame():
    frame = b"\x01\x02\x03payload"
    sock = FakeSocket(incoming=protocol.encode_frame(frame))
    assert Connection(sock).receive() == frame


def test_receive_reassembles_across_partial_recv():
    msg = Message(protocol.CONNECT, server="s")
    sock = FakeSocket(incoming=protocol.encode_message(msg))
    conn = Connection(sock, recv_size=3)  # force many small reads
    assert conn.receive() == msg


def test_receive_multiple_messages_in_sequence():
    a = Message(protocol.REGISTER, id="a")
    b = Message(protocol.DISCONNECT)
    sock = FakeSocket(
        incoming=protocol.encode_message(a) + protocol.encode_message(b)
    )
    conn = Connection(sock)
    assert conn.receive() == a
    assert conn.receive() == b


def test_receive_returns_none_on_peer_close():
    sock = FakeSocket(incoming=b"")
    assert Connection(sock).receive() is None


def test_close_delegates_to_socket():
    sock = FakeSocket()
    Connection(sock).close()
    assert sock.closed

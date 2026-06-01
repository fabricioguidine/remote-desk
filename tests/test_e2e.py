"""End-to-end test of the portable core over a real loopback TCP socket.

This wires the protocol, Connection framing, lz4 compression, and relay token
auth together exactly as the documented data flow uses them, without any
display, fixed port, or external network. It runs identically on Linux, macOS,
and Windows.
"""
import socket
import threading

from desktop.common import protocol
from desktop.common.connection import Connection
from desktop.common.compression import compress, decompress
from desktop.common.protocol import Message
from relay.auth import validate_token

TOKEN = "shared-secret"


def _relay_server(listener, results):
    """Minimal relay role: authenticate, ack, then stream one compressed frame."""
    raw, _ = listener.accept()
    with raw:
        conn = Connection(raw)
        register = conn.receive()
        results["register"] = register
        ok = validate_token(register.fields.get("token", ""), TOKEN)
        results["auth_ok"] = ok
        if not ok:
            conn.send_message(Message(protocol.ERROR, detail="bad token"))
            return
        conn.send_message(Message(protocol.REGISTER, status="registered"))
        # Send a screen frame: compress synthetic pixel bytes, frame it.
        pixels = bytes([i % 256 for i in range(4096)])
        conn.send_frame(compress(pixels))
        results["sent_pixels"] = pixels


def _run_session():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))  # ephemeral port
    listener.listen(1)
    host, port = listener.getsockname()

    results = {}
    server_thread = threading.Thread(
        target=_relay_server, args=(listener, results), daemon=True
    )
    server_thread.start()

    client_sock = socket.create_connection((host, port))
    client = Connection(client_sock)
    client.send_message(Message(protocol.REGISTER, id="desktop-server", token=TOKEN))
    ack = client.receive()
    frame = client.receive()
    client.close()
    server_thread.join(timeout=5)
    listener.close()
    return results, ack, frame


def test_authenticated_handshake_and_frame_stream():
    results, ack, frame = _run_session()
    assert results["auth_ok"] is True
    assert results["register"] == Message(
        protocol.REGISTER, id="desktop-server", token=TOKEN
    )
    assert ack == Message(protocol.REGISTER, status="registered")
    assert isinstance(frame, bytes)
    # The client recovers the exact pixels the server captured+compressed.
    assert decompress(frame) == results["sent_pixels"]


def test_rejected_token_yields_error_message():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    host, port = listener.getsockname()
    results = {}
    t = threading.Thread(
        target=_relay_server, args=(listener, results), daemon=True
    )
    t.start()

    client = Connection(socket.create_connection((host, port)))
    client.send_message(Message(protocol.REGISTER, id="x", token="wrong"))
    reply = client.receive()
    client.close()
    t.join(timeout=5)
    listener.close()

    assert results["auth_ok"] is False
    assert reply == Message(protocol.ERROR, detail="bad token")

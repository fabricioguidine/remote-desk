"""Connection - framed message transport.

Wraps a byte stream (e.g. a TCP socket or a WebSocket) so callers can send and
receive whole protocol messages and binary frames without worrying about
partial reads. The wire format is defined in protocol.py.

The production transport is WebSockets (see desktop/requirements.txt), imported
lazily so this module loads on any OS even without the optional dependency. The
framing logic here is transport-agnostic and is exercised end-to-end over a
loopback TCP socket in the tests.
"""
from . import protocol


class Connection:
    """Frames protocol messages over a blocking socket-like object.

    The socket only needs sendall(bytes) and recv(n) -> bytes, so a real
    socket.socket or any compatible stub works.
    """

    def __init__(self, sock, recv_size=65536):
        self._sock = sock
        self._recv_size = recv_size
        self._buffer = b""

    def send_message(self, message):
        self._sock.sendall(protocol.encode_message(message))

    def send_frame(self, data):
        self._sock.sendall(protocol.encode_frame(data))

    def receive(self):
        """Return the next Message or bytes frame, or None if the peer closed."""
        while True:
            item, self._buffer = protocol.decode(self._buffer)
            if item is not None:
                return item
            chunk = self._sock.recv(self._recv_size)
            if not chunk:
                return None
            self._buffer += chunk

    def close(self):
        self._sock.close()


def connect_websocket(url):  # pragma: no cover - requires network + websockets
    """Open a production WebSocket connection. Requires the websockets package."""
    try:
        import websockets.sync.client as ws_client
    except ImportError as exc:
        raise RuntimeError(
            "the 'websockets' package is required for WebSocket transport"
        ) from exc
    return ws_client.connect(url)

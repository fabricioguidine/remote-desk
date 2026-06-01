"""Compression - LZ4 helpers for frame payloads.

Pure and OS-agnostic. lz4 is a cross-platform dependency listed in
desktop/requirements.txt; it is imported lazily so this module imports even
where lz4 is not installed, and a clear error is raised only on use.
"""

try:
    import lz4.frame as _lz4
except ImportError:  # pragma: no cover - exercised only without lz4 installed
    _lz4 = None


def _require_lz4():
    if _lz4 is None:
        raise RuntimeError("lz4 is required for compression but is not installed")
    return _lz4


def compress(data):
    """Compress bytes with LZ4 frame format."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("compress expects bytes")
    return _require_lz4().compress(bytes(data))


def decompress(data):
    """Decompress LZ4-frame bytes produced by compress()."""
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("decompress expects bytes")
    return _require_lz4().decompress(bytes(data))

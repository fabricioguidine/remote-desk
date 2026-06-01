"""Tests for the LZ4 compression helpers."""
import pytest

from desktop.common import compression


def test_round_trip_repetitive_data():
    data = b"remote-desk-frame-" * 500
    compressed = compression.compress(data)
    assert isinstance(compressed, bytes)
    assert compression.decompress(compressed) == data


def test_round_trip_empty():
    assert compression.decompress(compression.compress(b"")) == b""


def test_round_trip_binary_payload():
    data = bytes(range(256)) * 16
    assert compression.decompress(compression.compress(data)) == data


def test_compress_reduces_size_for_repetitive_input():
    data = b"\x00" * 10000
    assert len(compression.compress(data)) < len(data)


def test_compress_accepts_bytearray():
    data = bytearray(b"abc" * 100)
    assert compression.decompress(compression.compress(data)) == bytes(data)


def test_compress_rejects_str():
    with pytest.raises(TypeError):
        compression.compress("not bytes")


def test_decompress_rejects_str():
    with pytest.raises(TypeError):
        compression.decompress("not bytes")

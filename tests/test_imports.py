"""Portability guarantee: every tracked module imports cleanly, headless, on
any OS. Platform-gated modules (screen capture, input, GUI, tray) must not
crash on import even when their OS-/display-specific dependencies are absent.
"""
import importlib

import pytest

PORTABLE_MODULES = [
    "desktop.common.protocol",
    "desktop.common.connection",
    "desktop.common.compression",
    "desktop.common.config",
    "relay.auth",
    "relay.config",
    "relay.handler",
    "relay.server",
]

# These pull in mss/pynput/pygame/pystray; they are skeletons today, so they
# must at least import without a display or those optional packages installed.
PLATFORM_GATED_MODULES = [
    "desktop.server.screen",
    "desktop.server.input",
    "desktop.server.tray",
    "desktop.server.gui",
    "desktop.server.app",
    "desktop.server.main",
    "desktop.client.viewer",
    "desktop.client.input",
    "desktop.client.gui",
    "desktop.client.app",
    "desktop.client.main",
]


@pytest.mark.parametrize("name", PORTABLE_MODULES)
def test_portable_module_imports(name):
    importlib.import_module(name)


@pytest.mark.parametrize("name", PLATFORM_GATED_MODULES)
def test_platform_gated_module_imports(name):
    importlib.import_module(name)


def test_compression_reports_missing_lz4(monkeypatch):
    from desktop.common import compression

    monkeypatch.setattr(compression, "_lz4", None)
    with pytest.raises(RuntimeError, match="lz4 is required"):
        compression.compress(b"data")

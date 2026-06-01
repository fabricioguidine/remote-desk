<div align="center">

<img src=".github/assets/banner.svg" alt="remote-desk banner" width="100%">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org)

[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](#cross-platform-support)

[![CI](https://github.com/fabricioguidine/remote-desk/actions/workflows/ci.yml/badge.svg)](https://github.com/fabricioguidine/remote-desk/actions/workflows/ci.yml)

</div>

> Open-source remote desktop that routes screen and input over a WebSocket relay server. The portable core (protocol, compression, config, connection, relay auth) runs on Linux, macOS, and Windows; screen capture and input require a desktop session (see [Cross-platform support](#cross-platform-support)).

remote-desk is a three-tier remote access tool: a desktop **server** captures the screen and executes incoming input, a desktop **client** displays the stream and captures local mouse/keyboard, and a lightweight **relay** server brokers traffic between them so connections work across NAT and over the internet. This repository is an early-stage scaffold: the project structure, module layout, dependencies, and architecture are in place, while the Python modules are currently skeleton files awaiting implementation (see [STATUS.md](STATUS.md)).

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Cross-platform support](#cross-platform-support)
- [Project structure](#project-structure)
- [License](#license)

## Features

- View a remote Windows desktop and control its mouse and keyboard.
- Relay-based connectivity for NAT traversal over the internet (client and server connect outbound to a shared relay).
- Screen capture via `mss` (no administrator privileges required).
- Frame encoding with Pillow (JPEG) and additional `lz4` compression.
- Frame rendering on the client with `pygame`.
- Remote input capture and execution with `pynput`.
- System tray integration on the server via `pystray`.
- Token-based authentication validated at the relay, with TLS intended for production deployments.
- JSON configuration via `desktop/config.example.json` (relay URL, token, capture FPS, quality, scale, monitor selection, client hotkeys).
- PyInstaller build scripts for producing standalone executables.

> Note: modules are scaffolded but not yet implemented. The features above describe the intended, documented design as reflected in the module layout, requirements, and `docs/ARCHITECTURE.md`.

## Architecture

The system has three components. The desktop **server** runs on the machine being controlled, the desktop **client** runs on the controlling machine, and the **relay** routes messages between them over WebSockets.

```mermaid
flowchart LR
    subgraph Client["Desktop Client (controlling PC)"]
        Viewer["viewer.py<br/>pygame rendering"]
        CInput["input.py<br/>capture mouse/keyboard"]
        CGUI["gui.py / app.py"]
    end

    subgraph Relay["Relay Server (VPS)"]
        RServer["server.py<br/>WebSocket server"]
        Handler["handler.py<br/>routing / sessions"]
        Auth["auth.py<br/>token validation"]
    end

    subgraph Server["Desktop Server (controlled PC)"]
        Screen["screen.py<br/>capture via mss"]
        SInput["input.py<br/>execute via pynput"]
        Tray["tray.py / app.py"]
    end

    Screen -->|"frames (JPEG + lz4)"| Handler
    Handler -->|"frames"| Viewer
    CInput -->|"input events"| Handler
    Handler -->|"input events"| SInput
    Auth -.->|"validates token"| Handler
```

A typical session, following the connection and streaming flow described in `docs/ARCHITECTURE.md`:

```mermaid
sequenceDiagram
    participant S as Desktop Server
    participant R as Relay
    participant C as Desktop Client

    S->>R: connect + register (token)
    R->>S: registered
    C->>R: connect + request server list (token)
    R->>C: server list
    C->>R: select server
    R-->>S: pair with client
    R-->>C: pair with server

    loop streaming
        S->>S: capture screen (mss)
        S->>S: encode JPEG + lz4
        S->>R: frame
        R->>C: frame
        C->>C: decompress + render (pygame)
    end

    loop control
        C->>C: capture input (pynput)
        C->>R: input event
        R->>S: input event
        S->>S: execute input (pynput)
    end
```

Shared concerns live in `desktop/common/`: the wire `protocol`, `connection` management, `compression`, and `config` loading.

## Requirements

- Python 3.10+ (CI covers 3.11, 3.12, 3.13)
- The desktop client and server need a desktop session for screen capture and
  input; the GUI features target Windows but the portable core runs on Linux,
  macOS, and Windows.
- A Linux VPS (recommended) for the relay server

Desktop dependencies (`desktop/requirements.txt`): `websockets`, `mss`, `Pillow`, `pynput`, `lz4`, `pygame`, `pystray`, `pyinstaller`.

Relay dependencies (`relay/requirements.txt`): `websockets`.

## Installation

### Windows (PowerShell)

```powershell
git clone https://github.com/fabricioguidine/remote-desk.git
Set-Location remote-desk

python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install desktop dependencies (client and server)
pip install -r desktop\requirements.txt
```

### Linux / macOS

```bash
git clone https://github.com/fabricioguidine/remote-desk.git
cd remote-desk

python3 -m venv .venv
. .venv/bin/activate

# Install desktop dependencies (client and server)
pip install -r desktop/requirements.txt
```

On the relay host (Linux VPS), only the relay dependency is needed:

```bash
pip install -r relay/requirements.txt
```

To configure a desktop install, copy the example config and edit it:

```powershell
Copy-Item desktop\config.example.json desktop\config.json
```

## Usage

Run the relay on the VPS:

```bash
python -m relay.server
```

Run the server on the Windows PC to be controlled:

```powershell
python -m desktop.server.main
```

Run the client on the Windows PC that controls:

```powershell
python -m desktop.client.main
```

Build standalone executables with PyInstaller:

```powershell
python scripts\build_server.py
python scripts\build_client.py
python scripts\build_relay.py
```

## Testing

The portable core is covered by a hermetic, OS-agnostic test suite that runs on
Linux, macOS, and Windows without a display, fixed port, or external network.

```bash
pip install -r requirements-dev.txt
pytest
```

The suite exercises (with synthetic data, `tmp_path`, and loopback sockets on an
ephemeral port):

- **Protocol** — JSON message and binary frame (de)serialization, the
  length-prefixed wire envelope, partial/incomplete reads, mixed streams, and
  error handling.
- **Compression** — LZ4 round-trips for binary payloads.
- **Config** — JSON loading/validation, default home-based path, defaults
  merging, and validation of `desktop/config.example.json`.
- **Connection** — framed send/receive with reassembly across partial reads.
- **Relay auth** — constant-time token validation (via the end-to-end test).
- **End-to-end** — a real client and relay role handshake over a loopback TCP
  socket: token auth, ack, and a compressed frame the client decompresses back
  to the exact captured bytes.
- **Importability** — every module (including the platform-gated stubs) imports
  cleanly headless on any OS.

CI runs this suite on a matrix of `ubuntu-latest`, `macos-latest`, and
`windows-latest` against Python 3.11, 3.12, and 3.13.

## Cross-platform support

The portable core is written to behave identically on Linux, macOS, and Windows:

- Paths use `pathlib`; the default config path derives from `Path.home()` (not
  the `HOME` env var, which is unset on Windows).
- Files are read as UTF-8 explicitly, independent of the platform default
  encoding.
- The optional `lz4` import is lazy, so `desktop.common.compression` imports on
  any OS and raises a clear error only if compression is used without `lz4`.
- The production WebSocket transport is imported lazily in
  `desktop.common.connection`, so the framing logic is testable without the
  `websockets` package.

### Platform-gated features

These require a real desktop session and cannot run in headless CI:

- **Screen capture** (`desktop/server/screen.py`, `mss`) — needs a real display.
- **Input capture/execution** (`desktop/{client,server}/input.py`, `pynput`) —
  needs a desktop session.
- **Client rendering** (`desktop/client/viewer.py`, `pygame`) and the
  **system tray** (`desktop/server/tray.py`, `pystray`) — need a desktop GUI.

These modules are scaffolded so they import cleanly everywhere; their
display-dependent behavior is intentionally not exercised by the test suite.

## Project structure

```
remote-desk/
├── relay/                  # WebSocket relay server (VPS)
│   ├── server.py           # WebSocket server, routes connections
│   ├── handler.py          # Message routing and session management
│   ├── auth.py             # Token validation
│   └── config.py           # Relay configuration
├── desktop/
│   ├── client/             # Controlling-side viewer and input capture
│   │   ├── main.py         # Client entry point
│   │   ├── app.py          # Client application logic
│   │   ├── viewer.py       # Screen display (pygame)
│   │   ├── input.py        # Mouse/keyboard capture
│   │   └── gui.py          # Client GUI
│   ├── server/             # Controlled-side capture and input execution
│   │   ├── main.py         # Server entry point
│   │   ├── app.py          # Server application logic
│   │   ├── screen.py       # Screen capture (mss)
│   │   ├── input.py        # Input execution (pynput)
│   │   ├── tray.py         # System tray icon (pystray)
│   │   └── gui.py          # Server GUI
│   ├── common/             # Shared modules
│   │   ├── protocol.py     # Message classes and serialization
│   │   ├── connection.py   # WebSocket connection management
│   │   ├── compression.py  # LZ4 compression utilities
│   │   └── config.py       # Configuration loading
│   └── config.example.json # Example configuration
├── scripts/                # PyInstaller build and cert generation scripts
├── tests/                  # Unit tests (protocol, connection, compression)
└── docs/                   # Architecture, setup, and usage documentation
```

## License

Released under the [MIT License](LICENSE).

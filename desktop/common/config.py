"""Config - configuration loading and validation.

Loads the JSON config documented in desktop/config.example.json. Paths use
pathlib and files are read as UTF-8 so behavior is identical on Linux, macOS,
and Windows. Pure and OS-agnostic.
"""
import json
from pathlib import Path

REQUIRED_SECTIONS = ("connection", "server", "client")

DEFAULTS = {
    "connection": {"reconnect_interval": 5, "timeout": 30},
    "server": {"capture_fps": 30, "quality": 70, "scale": 1.0, "monitor": 0},
    "client": {"show_fps": True, "show_latency": True},
}


class ConfigError(Exception):
    """Raised when a configuration file is missing required fields."""


def default_config_path():
    """Path to the user's config, resolved from the home directory on every OS."""
    return Path.home() / ".config" / "remote-desk" / "config.json"


def _apply_defaults(config):
    merged = {section: dict(values) for section, values in DEFAULTS.items()}
    for section, values in config.items():
        if isinstance(values, dict):
            merged.setdefault(section, {}).update(values)
        else:
            merged[section] = values
    return merged


def validate(config):
    """Validate required sections and the relay token. Returns config with defaults."""
    if not isinstance(config, dict):
        raise ConfigError("config must be a JSON object")
    for section in REQUIRED_SECTIONS:
        if section not in config:
            raise ConfigError(f"missing required section: {section}")
    connection = config["connection"]
    if not connection.get("relay_url"):
        raise ConfigError("connection.relay_url is required")
    if not connection.get("token"):
        raise ConfigError("connection.token is required")
    return _apply_defaults(config)


def load_config(path=None):
    """Load and validate the JSON config at path (or the default path)."""
    path = Path(path) if path is not None else default_config_path()
    if not path.exists():
        raise ConfigError(f"config file not found: {path}")
    with open(path, encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"invalid JSON in {path}: {exc}") from exc
    return validate(data)

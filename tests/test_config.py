"""Tests for configuration loading and validation."""
import json
from pathlib import Path

import pytest

from desktop.common import config
from desktop.common.config import ConfigError


def _minimal():
    return {
        "connection": {"relay_url": "wss://relay:8443", "token": "shared"},
        "server": {},
        "client": {},
    }


def test_default_config_path_under_home():
    path = config.default_config_path()
    assert isinstance(path, Path)
    assert path.name == "config.json"
    assert path.parent.name == "remote-desk"
    assert Path.home() in path.parents


def test_validate_applies_defaults():
    result = config.validate(_minimal())
    assert result["server"]["capture_fps"] == 30
    assert result["server"]["quality"] == 70
    assert result["connection"]["timeout"] == 30
    # provided values are preserved
    assert result["connection"]["relay_url"] == "wss://relay:8443"


def test_validate_preserves_overrides():
    cfg = _minimal()
    cfg["server"]["capture_fps"] = 15
    result = config.validate(cfg)
    assert result["server"]["capture_fps"] == 15


@pytest.mark.parametrize("section", ["connection", "server", "client"])
def test_validate_missing_section_raises(section):
    cfg = _minimal()
    del cfg[section]
    with pytest.raises(ConfigError, match=section):
        config.validate(cfg)


def test_validate_missing_relay_url_raises():
    cfg = _minimal()
    del cfg["connection"]["relay_url"]
    with pytest.raises(ConfigError, match="relay_url"):
        config.validate(cfg)


def test_validate_missing_token_raises():
    cfg = _minimal()
    del cfg["connection"]["token"]
    with pytest.raises(ConfigError, match="token"):
        config.validate(cfg)


def test_load_config_reads_and_validates(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps(_minimal()), encoding="utf-8")
    result = config.load_config(cfg_file)
    assert result["connection"]["token"] == "shared"
    assert result["server"]["monitor"] == 0


def test_load_config_unicode(tmp_path):
    cfg = _minimal()
    cfg["server"]["id"] = "São-Paulo-PC"
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text(json.dumps(cfg, ensure_ascii=False), encoding="utf-8")
    assert config.load_config(cfg_file)["server"]["id"] == "São-Paulo-PC"


def test_load_config_missing_file_raises(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        config.load_config(tmp_path / "nope.json")


def test_load_config_invalid_json_raises(tmp_path):
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text("{ not json", encoding="utf-8")
    with pytest.raises(ConfigError, match="invalid JSON"):
        config.load_config(cfg_file)


def test_example_config_is_valid():
    example = Path(__file__).resolve().parent.parent / "desktop" / "config.example.json"
    with open(example, encoding="utf-8") as handle:
        data = json.load(handle)
    result = config.validate(data)
    assert result["connection"]["relay_url"]

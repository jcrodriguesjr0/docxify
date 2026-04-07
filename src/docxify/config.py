"""Configuration loading from TOML files."""

from __future__ import annotations

import sys
from dataclasses import fields
from pathlib import Path
from typing import Any

from .styles import StyleProfile, PRESETS

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]


CONFIG_FILENAMES = ["docxify.toml", ".docxify.toml"]
USER_CONFIG_PATH = Path.home() / ".config" / "docxify" / "config.toml"


def find_config(start_dir: str | Path | None = None) -> Path | None:
    """Find the nearest docxify.toml walking up from start_dir."""
    search = Path(start_dir) if start_dir else Path.cwd()

    for directory in [search, *search.parents]:
        for name in CONFIG_FILENAMES:
            candidate = directory / name
            if candidate.is_file():
                return candidate

    if USER_CONFIG_PATH.is_file():
        return USER_CONFIG_PATH

    return None


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    """Load and parse a TOML config file."""
    if config_path is None:
        found = find_config()
        if found is None:
            return {}
        config_path = found

    path = Path(config_path)
    if not path.is_file():
        return {}

    with open(path, "rb") as f:
        return tomllib.load(f)


def style_from_config(config: dict[str, Any]) -> StyleProfile:
    """Build a StyleProfile from config dict.

    Supports a "preset" key to start from a named preset,
    then overrides individual fields.
    """
    style_section = config.get("style", {})
    preset_name = style_section.pop("preset", "default") if isinstance(style_section, dict) else "default"

    base = PRESETS.get(preset_name, PRESETS["default"])

    if not style_section:
        return base

    # Override fields
    valid_fields = {f.name for f in fields(StyleProfile)}
    overrides = {k: v for k, v in style_section.items() if k in valid_fields}

    return StyleProfile(**{**{f.name: getattr(base, f.name) for f in fields(StyleProfile)}, **overrides})


def generate_default_config() -> str:
    """Generate a starter docxify.toml content."""
    return '''# docxify configuration
# Docs: https://github.com/yourusername/docxify

[style]
# preset = "default"  # Options: default, compact, academic, modern
# font_name = "Calibri"
# body_size = 11
# h1_size = 22
# h2_size = 16
# h3_size = 14
# code_font = "Courier New"
# code_size = 10
# language = "en-US"

# Page (A4 default)
# page_width_cm = 21.0
# page_height_cm = 29.7
# margin_top_cm = 2.54
# margin_bottom_cm = 2.54
# margin_left_cm = 2.54
# margin_right_cm = 2.54

# Heading alignment
# h1_align = "center"
# h2_align = "left"
'''

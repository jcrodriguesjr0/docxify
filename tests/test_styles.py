"""Tests for style profiles."""

from docxify.styles import StyleProfile, PRESETS


def test_default_preset_exists():
    assert "default" in PRESETS


def test_heading_sizes():
    style = StyleProfile()
    assert style.heading_size(1) == 22
    assert style.heading_size(2) == 16
    assert style.heading_size(6) == 11
    assert style.heading_size(99) == style.body_size


def test_heading_align():
    style = StyleProfile(h1_align="center", h2_align="left")
    assert style.heading_align(1) == "center"
    assert style.heading_align(2) == "left"
    assert style.heading_align(3) == "left"


def test_presets_are_valid():
    for name, style in PRESETS.items():
        assert style.font_name
        assert style.body_size > 0
        assert style.page_width_cm > 0

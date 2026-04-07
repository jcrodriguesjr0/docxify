"""CLI entry point using click."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from . import __version__
from .converter import convert
from .extractor import extract_to_file
from .batch import batch_convert, batch_extract, BatchResult
from .config import load_config, style_from_config, generate_default_config, find_config
from .styles import StyleProfile, PRESETS


def _resolve_style(preset: str | None, font: str | None, body_size: int | None) -> StyleProfile:
    """Build a StyleProfile from config file + CLI overrides."""
    config = load_config()
    style = style_from_config(config)

    if preset and preset in PRESETS:
        style = PRESETS[preset]

    if font:
        style.font_name = font
    if body_size:
        style.body_size = body_size

    return style


@click.group()
@click.version_option(__version__, prog_name="docxify")
def app():
    """docxify - Convert AI-generated markdown to professional .docx files."""
    pass


@app.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), default=None, help="Output .docx path (default: same name as input).")
@click.option("--preset", type=click.Choice(list(PRESETS.keys())), default=None, help="Style preset.")
@click.option("--font", default=None, help="Override font name.")
@click.option("--body-size", type=int, default=None, help="Override body font size (pt).")
@click.option("--template", type=click.Path(exists=True), default=None, help="Use a .docx template.")
def convert_cmd(input_file: str, output: str | None, preset: str | None, font: str | None, body_size: int | None, template: str | None):
    """Convert a markdown file to .docx."""
    input_path = Path(input_file)
    if output is None:
        output = str(input_path.with_suffix(".docx"))

    style = _resolve_style(preset, font, body_size)
    md_text = input_path.read_text(encoding="utf-8")
    result = convert(md_text, output, style=style, template=template)
    click.echo(f"Created: {result}")


@app.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), default=None, help="Output .md path (default: same name as input).")
def extract_cmd(input_file: str, output: str | None):
    """Extract a .docx file to markdown."""
    input_path = Path(input_file)
    if output is None:
        output = str(input_path.with_suffix(".md"))

    result = extract_to_file(input_path, output)
    click.echo(f"Created: {result}")


@app.command()
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False))
@click.option("-o", "--output", type=click.Path(), required=True, help="Output directory.")
@click.option("--pattern", default="*.md", help="Glob pattern for input files.")
@click.option("--reverse", is_flag=True, help="Extract .docx -> .md instead.")
@click.option("--preset", type=click.Choice(list(PRESETS.keys())), default=None, help="Style preset.")
@click.option("--font", default=None, help="Override font name.")
@click.option("--body-size", type=int, default=None, help="Override body font size (pt).")
def batch_cmd(input_dir: str, output: str, pattern: str, reverse: bool, preset: str | None, font: str | None, body_size: int | None):
    """Batch convert a directory of files."""
    if reverse:
        if pattern == "*.md":
            pattern = "*.docx"
        result = batch_extract(input_dir, output, pattern=pattern)
    else:
        style = _resolve_style(preset, font, body_size)
        result = batch_convert(input_dir, output, pattern=pattern, style=style)

    _print_batch_result(result)


@app.command("init")
def init_cmd():
    """Create a starter docxify.toml config file."""
    target = Path.cwd() / "docxify.toml"
    if target.exists():
        click.echo(f"Config already exists: {target}")
        return

    target.write_text(generate_default_config(), encoding="utf-8")
    click.echo(f"Created: {target}")


@app.command("presets")
def presets_cmd():
    """List available style presets."""
    for name, style in PRESETS.items():
        click.echo(f"  {name:12s}  {style.font_name} {style.body_size}pt, "
                    f"h1={style.h1_size}pt, margins={style.margin_left_cm}cm")


def _print_batch_result(result: BatchResult) -> None:
    click.echo(f"Converted: {result.success_count}/{result.total}")
    for path in result.converted:
        click.echo(f"  + {path}")
    for path, error in result.failed:
        click.echo(f"  x {path}: {error}", err=True)

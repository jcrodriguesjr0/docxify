"""Batch conversion operations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .styles import StyleProfile
from .converter import convert
from .extractor import extract_to_file


@dataclass
class BatchResult:
    """Result of a batch operation."""
    converted: list[Path]
    failed: list[tuple[Path, str]]

    @property
    def total(self) -> int:
        return len(self.converted) + len(self.failed)

    @property
    def success_count(self) -> int:
        return len(self.converted)


def batch_convert(
    input_dir: str | Path,
    output_dir: str | Path,
    pattern: str = "*.md",
    style: StyleProfile | None = None,
    template: str | None = None,
) -> BatchResult:
    """Convert all matching markdown files in a directory to .docx.

    Args:
        input_dir: Directory containing .md files.
        output_dir: Directory for .docx output.
        pattern: Glob pattern for input files.
        style: Optional style profile.
        template: Optional .docx template path.

    Returns:
        BatchResult with converted files and any failures.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    converted: list[Path] = []
    failed: list[tuple[Path, str]] = []

    for md_file in sorted(input_path.glob(pattern)):
        docx_name = md_file.stem + ".docx"
        docx_path = output_path / docx_name
        try:
            md_text = md_file.read_text(encoding="utf-8")
            convert(md_text, docx_path, style=style, template=template)
            converted.append(docx_path)
        except Exception as e:
            failed.append((md_file, str(e)))

    return BatchResult(converted=converted, failed=failed)


def batch_extract(
    input_dir: str | Path,
    output_dir: str | Path,
    pattern: str = "*.docx",
) -> BatchResult:
    """Extract all matching .docx files in a directory to markdown.

    Args:
        input_dir: Directory containing .docx files.
        output_dir: Directory for .md output.
        pattern: Glob pattern for input files.

    Returns:
        BatchResult with converted files and any failures.
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    converted: list[Path] = []
    failed: list[tuple[Path, str]] = []

    for docx_file in sorted(input_path.glob(pattern)):
        md_name = docx_file.stem + ".md"
        md_path = output_path / md_name
        try:
            extract_to_file(docx_file, md_path)
            converted.append(md_path)
        except Exception as e:
            failed.append((docx_file, str(e)))

    return BatchResult(converted=converted, failed=failed)

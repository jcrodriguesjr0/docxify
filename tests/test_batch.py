"""Tests for batch operations."""

from pathlib import Path
from docxify.batch import batch_convert, batch_extract


def test_batch_convert(tmp_path):
    # Create input files
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "a.md").write_text("# File A\n\nContent A", encoding="utf-8")
    (input_dir / "b.md").write_text("# File B\n\nContent B", encoding="utf-8")

    output_dir = tmp_path / "output"
    result = batch_convert(input_dir, output_dir)

    assert result.success_count == 2
    assert result.total == 2
    assert (output_dir / "a.docx").exists()
    assert (output_dir / "b.docx").exists()


def test_batch_extract(tmp_path):
    # First create docx files via batch_convert
    input_dir = tmp_path / "md_input"
    input_dir.mkdir()
    (input_dir / "a.md").write_text("# File A\n\nContent A", encoding="utf-8")

    docx_dir = tmp_path / "docx"
    batch_convert(input_dir, docx_dir)

    md_output = tmp_path / "md_output"
    result = batch_extract(docx_dir, md_output)

    assert result.success_count == 1
    assert (md_output / "a.md").exists()


def test_batch_empty_dir(tmp_path):
    input_dir = tmp_path / "empty"
    input_dir.mkdir()
    output_dir = tmp_path / "output"

    result = batch_convert(input_dir, output_dir)
    assert result.total == 0

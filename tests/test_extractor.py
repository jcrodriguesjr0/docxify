"""Tests for DOCX -> MD extraction."""

from docxify.converter import convert
from docxify.extractor import extract, extract_to_file


def test_roundtrip(sample_md, tmp_docx, tmp_md):
    """Convert md->docx->md and check key content survives."""
    convert(sample_md, tmp_docx)
    result = extract_to_file(tmp_docx, tmp_md)
    assert result.exists()

    extracted = result.read_text(encoding="utf-8")
    assert "Project Report" in extracted
    assert "Executive Summary" in extracted
    assert "First bullet point" in extracted


def test_extract_returns_string(sample_md, tmp_docx):
    convert(sample_md, tmp_docx)
    md = extract(tmp_docx)
    assert isinstance(md, str)
    assert len(md) > 0
    assert md.endswith("\n")


def test_extract_no_excessive_blanks(sample_md, tmp_docx):
    convert(sample_md, tmp_docx)
    md = extract(tmp_docx)
    assert "\n\n\n" not in md

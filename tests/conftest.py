"""Shared test fixtures."""

import pytest
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_md():
    return (FIXTURES_DIR / "sample.md").read_text(encoding="utf-8")


@pytest.fixture
def tmp_docx(tmp_path):
    return tmp_path / "output.docx"


@pytest.fixture
def tmp_md(tmp_path):
    return tmp_path / "output.md"

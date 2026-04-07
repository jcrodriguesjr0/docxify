"""docxify - Convert AI-generated markdown to professional .docx files."""

__version__ = "0.1.0"

from .converter import convert
from .extractor import extract, extract_to_file
from .styles import StyleProfile, PRESETS
from .batch import batch_convert, batch_extract

__all__ = [
    "convert",
    "extract",
    "extract_to_file",
    "StyleProfile",
    "PRESETS",
    "batch_convert",
    "batch_extract",
]

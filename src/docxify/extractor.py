"""DOCX -> Markdown extraction engine."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


def _paragraph_is_heading(paragraph) -> tuple[bool, int]:
    """Detect if a paragraph is a heading and return its level."""
    style_name = (paragraph.style.name or "").lower()
    if style_name.startswith("heading"):
        try:
            level = int(style_name.replace("heading", "").strip())
            return True, level
        except ValueError:
            pass
    # Heuristic: bold + larger font = heading
    if paragraph.runs:
        first_run = paragraph.runs[0]
        if first_run.bold and first_run.font.size and first_run.font.size.pt >= 14:
            return True, 1 if first_run.font.size.pt >= 20 else 2
    return False, 0


def _runs_to_markdown(paragraph) -> str:
    """Convert paragraph runs to markdown with inline formatting."""
    parts: list[str] = []
    for run in paragraph.runs:
        text = run.text
        if not text:
            continue

        is_code = run.font.name and "courier" in run.font.name.lower()
        is_bold = run.bold
        is_italic = run.italic

        if is_code:
            parts.append(f"`{text}`")
        elif is_bold and is_italic:
            parts.append(f"***{text}***")
        elif is_bold:
            parts.append(f"**{text}**")
        elif is_italic:
            parts.append(f"*{text}*")
        else:
            parts.append(text)

    return "".join(parts)


def _is_bullet(paragraph) -> bool:
    """Check if paragraph has bullet formatting."""
    text = paragraph.text.strip()
    if text.startswith(("\u2022 ", "- ", "* ")):
        return True
    # Check XML for list numbering
    pPr = paragraph._element.pPr
    if pPr is not None:
        numPr = pPr.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr"
        )
        if numPr is not None:
            return True
    return False


def extract(docx_path: str | Path) -> str:
    """Extract a .docx file to markdown.

    Args:
        docx_path: Path to the .docx file.

    Returns:
        Markdown string.
    """
    doc = Document(str(docx_path))
    lines: list[str] = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if not text:
            lines.append("")
            continue

        is_heading, level = _paragraph_is_heading(paragraph)
        if is_heading:
            prefix = "#" * level
            lines.append(f"{prefix} {text}")
            lines.append("")
            continue

        if _is_bullet(paragraph):
            clean = text.lstrip("\u2022-* ").strip()
            md_text = _runs_to_markdown(paragraph)
            # Remove bullet char from md_text too
            for prefix in ("\u2022 ", "- ", "* "):
                if md_text.startswith(prefix):
                    md_text = md_text[len(prefix):]
                    break
            lines.append(f"- {md_text}")
            continue

        md_text = _runs_to_markdown(paragraph)
        lines.append(md_text)

    # Clean up excessive blank lines
    result: list[str] = []
    prev_blank = False
    for line in lines:
        if not line.strip():
            if not prev_blank:
                result.append("")
            prev_blank = True
        else:
            result.append(line)
            prev_blank = False

    return "\n".join(result).strip() + "\n"


def extract_to_file(
    docx_path: str | Path,
    output_path: str | Path,
) -> Path:
    """Extract a .docx file and save as .md.

    Args:
        docx_path: Path to the .docx file.
        output_path: Where to save the .md file.

    Returns:
        Path to the generated .md file.
    """
    md_content = extract(docx_path)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(md_content, encoding="utf-8")
    return path

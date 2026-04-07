"""Markdown parser that produces an intermediate representation.

Converts raw markdown text into a list of typed nodes that the converter
can render into any output format.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


# --- Inline runs ---

class RunStyle(Enum):
    NORMAL = auto()
    BOLD = auto()
    ITALIC = auto()
    BOLD_ITALIC = auto()
    CODE = auto()


@dataclass
class TextRun:
    """A segment of text with a single style."""
    text: str
    style: RunStyle = RunStyle.NORMAL


# --- Block nodes ---

@dataclass
class Heading:
    level: int  # 1-6
    runs: List[TextRun] = field(default_factory=list)


@dataclass
class Paragraph:
    runs: List[TextRun] = field(default_factory=list)


@dataclass
class BulletItem:
    runs: List[TextRun] = field(default_factory=list)
    indent_level: int = 0


@dataclass
class NumberedItem:
    number: int
    runs: List[TextRun] = field(default_factory=list)
    indent_level: int = 0


@dataclass
class CodeBlock:
    code: str
    language: str = ""


@dataclass
class BlockQuote:
    runs: List[TextRun] = field(default_factory=list)


@dataclass
class HorizontalRule:
    pass


@dataclass
class BlankLine:
    pass


Node = Heading | Paragraph | BulletItem | NumberedItem | CodeBlock | BlockQuote | HorizontalRule | BlankLine


# --- Inline parser ---

_INLINE_RE = re.compile(
    r"(`[^`]+`)"              # inline code
    r"|(\*\*\*[^*]+\*\*\*)"  # bold+italic
    r"|(\*\*[^*]+\*\*)"      # bold
    r"|(\*[^*]+\*)"          # italic
    r"|(__[^_]+__)"           # bold (underscore)
    r"|(_[^_]+_)"             # italic (underscore)
)


def parse_inline(text: str) -> List[TextRun]:
    """Parse inline markdown formatting into TextRuns."""
    runs: List[TextRun] = []
    pos = 0

    for match in _INLINE_RE.finditer(text):
        # Add any text before this match as normal
        if match.start() > pos:
            runs.append(TextRun(text[pos:match.start()]))

        matched = match.group()

        if matched.startswith("`"):
            runs.append(TextRun(matched[1:-1], RunStyle.CODE))
        elif matched.startswith("***") or matched.startswith("___"):
            runs.append(TextRun(matched[3:-3], RunStyle.BOLD_ITALIC))
        elif matched.startswith("**") or matched.startswith("__"):
            runs.append(TextRun(matched[2:-2], RunStyle.BOLD))
        elif matched.startswith("*") or matched.startswith("_"):
            runs.append(TextRun(matched[1:-1], RunStyle.ITALIC))

        pos = match.end()

    # Remaining text
    if pos < len(text):
        runs.append(TextRun(text[pos:]))

    return runs if runs else [TextRun(text)]


# --- Block parser ---

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)")
_BULLET_RE = re.compile(r"^(\s*)[*\-+]\s+(.*)")
_NUMBERED_RE = re.compile(r"^(\s*)(\d+)\.\s+(.*)")
_FENCE_RE = re.compile(r"^```(\w*)")
_BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)")
_HR_RE = re.compile(r"^(---+|\*\*\*+|___+)\s*$")


def parse_markdown(text: str) -> List[Node]:
    """Parse a markdown string into a list of block nodes."""
    lines = text.split("\n")
    nodes: List[Node] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Blank line
        if not stripped:
            nodes.append(BlankLine())
            i += 1
            continue

        # Horizontal rule
        if _HR_RE.match(stripped):
            nodes.append(HorizontalRule())
            i += 1
            continue

        # Fenced code block
        fence_match = _FENCE_RE.match(stripped)
        if fence_match:
            lang = fence_match.group(1)
            code_lines: list[str] = []
            i += 1
            while i < len(lines):
                if lines[i].strip().startswith("```"):
                    i += 1
                    break
                code_lines.append(lines[i])
                i += 1
            nodes.append(CodeBlock("\n".join(code_lines), lang))
            continue

        # Heading
        heading_match = _HEADING_RE.match(stripped)
        if heading_match:
            level = len(heading_match.group(1))
            content = heading_match.group(2).strip()
            nodes.append(Heading(level, parse_inline(content)))
            i += 1
            continue

        # Bullet list
        bullet_match = _BULLET_RE.match(line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            indent_level = indent // 2
            content = bullet_match.group(2).strip()
            nodes.append(BulletItem(parse_inline(content), indent_level))
            i += 1
            continue

        # Numbered list
        num_match = _NUMBERED_RE.match(line)
        if num_match:
            indent = len(num_match.group(1))
            indent_level = indent // 2
            number = int(num_match.group(2))
            content = num_match.group(3).strip()
            nodes.append(NumberedItem(number, parse_inline(content), indent_level))
            i += 1
            continue

        # Block quote
        bq_match = _BLOCKQUOTE_RE.match(stripped)
        if bq_match:
            content = bq_match.group(1)
            nodes.append(BlockQuote(parse_inline(content)))
            i += 1
            continue

        # Regular paragraph
        nodes.append(Paragraph(parse_inline(stripped)))
        i += 1

    return nodes

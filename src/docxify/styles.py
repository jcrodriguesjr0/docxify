"""Style profiles for document generation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StyleProfile:
    """All tunable styling parameters for document generation.

    Units:
      - font sizes: points (int)
      - margins: centimeters (float)
      - spacing: points (int)
    """

    # Font
    font_name: str = "Calibri"
    body_size: int = 11
    h1_size: int = 22
    h2_size: int = 16
    h3_size: int = 14
    h4_size: int = 12
    h5_size: int = 11
    h6_size: int = 11
    code_font: str = "Courier New"
    code_size: int = 10

    # Page dimensions (cm)
    page_width_cm: float = 21.0   # A4
    page_height_cm: float = 29.7  # A4
    margin_top_cm: float = 2.54
    margin_bottom_cm: float = 2.54
    margin_left_cm: float = 2.54
    margin_right_cm: float = 2.54

    # Spacing (points)
    space_before: int = 6
    space_after: int = 6
    line_spacing: float = 1.15

    # Heading alignment: "left" | "center"
    h1_align: str = "center"
    h2_align: str = "left"

    # Colors (hex without #)
    body_color: str = "000000"
    heading_color: str = "000000"
    code_bg_color: str = "F2F2F2"

    # Language (BCP 47)
    language: str = "en-US"

    def heading_size(self, level: int) -> int:
        sizes = {1: self.h1_size, 2: self.h2_size, 3: self.h3_size,
                 4: self.h4_size, 5: self.h5_size, 6: self.h6_size}
        return sizes.get(level, self.body_size)

    def heading_align(self, level: int) -> str:
        if level == 1:
            return self.h1_align
        return self.h2_align


# Common presets
PRESETS: dict[str, StyleProfile] = {
    "default": StyleProfile(),
    "compact": StyleProfile(
        body_size=10,
        h1_size=18,
        h2_size=14,
        h3_size=12,
        space_before=3,
        space_after=3,
        margin_top_cm=1.5,
        margin_bottom_cm=1.5,
        margin_left_cm=1.5,
        margin_right_cm=1.5,
    ),
    "academic": StyleProfile(
        font_name="Times New Roman",
        body_size=12,
        h1_size=14,
        h2_size=13,
        h3_size=12,
        h1_align="center",
        h2_align="left",
        line_spacing=2.0,
        margin_top_cm=2.54,
        margin_bottom_cm=2.54,
        margin_left_cm=3.0,
        margin_right_cm=2.54,
    ),
    "modern": StyleProfile(
        font_name="Inter",
        body_size=11,
        h1_size=24,
        h2_size=18,
        h3_size=14,
        heading_color="1A1A2E",
        space_before=8,
        space_after=4,
    ),
}

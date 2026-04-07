# docxify

**Convert AI-generated markdown to professional `.docx` files — and back.**

AI tools like ChatGPT, Claude, and Gemini output markdown. Your boss wants a Word doc. docxify bridges the gap.

## Features

- **MD → DOCX** — Headings, bold, italic, code blocks, bullets, numbered lists, blockquotes
- **DOCX → MD** — Extract text from Word docs back to clean markdown
- **Batch mode** — Convert entire folders at once
- **Style presets** — `default`, `compact`, `academic`, `modern` — or customize everything
- **Config file** — Set once in `docxify.toml`, forget forever
- **Template support** — Use your company's `.docx` template as a base
- **Zero bloat** — Only 3 dependencies: `python-docx`, `click`, `tomli`

## Install

```bash
pip install docxify
```

## Quick start

```bash
# Convert markdown to docx
docxify convert report.md

# Convert with a specific preset
docxify convert report.md --preset academic

# Convert with custom font
docxify convert report.md --font "Arial" --body-size 12

# Extract docx back to markdown
docxify extract document.docx

# Batch convert a folder
docxify batch ./markdown-files/ -o ./docx-output/

# Batch extract (docx -> md)
docxify batch ./docx-files/ -o ./md-output/ --reverse

# Generate a config file
docxify init

# List available presets
docxify presets
```

## Style presets

| Preset | Font | Body | H1 | Margins | Use case |
|--------|------|------|----|---------|----------|
| `default` | Calibri 11pt | 11pt | 22pt | 2.54cm | General purpose |
| `compact` | Calibri 10pt | 10pt | 18pt | 1.5cm | Dense reports |
| `academic` | Times New Roman 12pt | 12pt | 14pt | 2.54/3cm | Papers, essays |
| `modern` | Inter 11pt | 11pt | 24pt | 2.54cm | Startup docs |

## Configuration

Create a `docxify.toml` in your project root (or run `docxify init`):

```toml
[style]
preset = "default"
font_name = "Calibri"
body_size = 11
h1_size = 22
language = "en-US"
```

Config lookup order: `./docxify.toml` → parent dirs → `~/.config/docxify/config.toml`

Priority: CLI flags > config file > preset defaults.

## Python API

```python
import docxify

# Simple conversion
docxify.convert("# Hello\n\nWorld", "output.docx")

# With a style preset
from docxify import PRESETS
docxify.convert(markdown_text, "output.docx", style=PRESETS["academic"])

# Custom style
from docxify import StyleProfile
style = StyleProfile(font_name="Arial", body_size=12, language="pt-BR")
docxify.convert(markdown_text, "output.docx", style=style)

# Extract docx to markdown string
md = docxify.extract("document.docx")

# Batch
from docxify import batch_convert
result = batch_convert("./md-files/", "./output/")
print(f"Converted {result.success_count}/{result.total}")
```

## Use with AI tools

### ChatGPT / Claude workflow

1. Copy the AI's markdown response
2. Save to a `.md` file
3. Run `docxify convert response.md -o report.docx`

### Batch workflow (multiple conversations)

```bash
# Save all your AI outputs to a folder
ls ai-outputs/
#   meeting-notes.md
#   project-plan.md
#   code-review.md

# Convert all at once
docxify batch ai-outputs/ -o documents/ --preset modern
```

## Supported markdown

| Element | Syntax | Supported |
|---------|--------|-----------|
| Headings | `# H1` through `###### H6` | Yes |
| Bold | `**text**` or `__text__` | Yes |
| Italic | `*text*` or `_text_` | Yes |
| Bold+Italic | `***text***` | Yes |
| Inline code | `` `code` `` | Yes |
| Code blocks | ` ```lang ... ``` ` | Yes |
| Bullet lists | `- item` or `* item` | Yes |
| Numbered lists | `1. item` | Yes |
| Blockquotes | `> text` | Yes |
| Horizontal rules | `---` | Yes |
| Nested lists | Indented sub-items | Yes |

## License

MIT

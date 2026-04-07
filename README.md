# docxify

[🇺🇸 English](#english) | [🇧🇷 Português](#português)

---

<a name="english"></a>
## 🇺🇸 English Version

**Convert AI-generated markdown to professional `.docx` files — and back.**

AI tools like ChatGPT, Claude, and Gemini output markdown. Your boss wants a Word doc. docxify bridges the gap.

### Features

- **MD → DOCX** — Headings, bold, italic, code blocks, bullets, numbered lists, blockquotes
- **DOCX → MD** — Extract text from Word docs back to clean markdown
- **Batch mode** — Convert entire folders at once
- **Style presets** — `default`, `compact`, `academic`, `modern` — or customize everything
- **Config file** — Set once in `docxify.toml`, forget forever
- **Template support** — Use your company's `.docx` template as a base
- **Zero bloat** — Only 3 dependencies: `python-docx`, `click`, `tomli`

### Install

```bash
pip install docxify
```

### Quick start

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

### Supported markdown

| Element | Syntax | Supported |
|---------|--------|-----------|
| Headings | `# H1` through `###### H6` | Yes |
| Bold | `**text**` or `__text__` | Yes |
| Italic | `*text*` or `_text_` | Yes |
| Code | `code` blocks | Yes |

### License
MIT

---

<a name="português"></a>
## 🇧🇷 Versão em Português

**Converta markdown gerado por IA para arquivos `.docx` profissionais — e vice-versa.**

Ferramentas de IA como ChatGPT, Claude e Gemini cospem Markdown. O seu chefe / sua empresa usam Word. O `docxify` faz a ponte entre esses mundos com perfeição.

### 🚀 Funcionalidades

- **MD → DOCX** — Títulos, negrito, itálico, blocos de código, marcadores, listas e citações
- **DOCX → MD** — Extração limpa para voltar textos do Word para prompts/markdown
- **Modo em Lote (Batch)** — Converta pastas inteiras simultaneamente
- **Presets de Estilo** — `default`, `compact`, `academic`, `modern` — ou parametrize tudo ao seu favor
- **Arquivo de Config.** — Configure uma vez no respositório via `docxify.toml`
- **Suporte a Template** — Injete o layout da sua própria empresa como base estrutural
- **Extremamente Leve** — Apenas 3 dependências ativas: `python-docx`, `click`, `tomli`

### 💻 Instalação

```bash
pip install docxify
```

### ⚡ Uso Rápido e CLI

```bash
# Converter markdown puro em docx
docxify convert report.md

# Usar um preset acadêmico ou corporativo
docxify convert report.md --preset academic

# Formatar uma CLI customizada na marra
docxify convert report.md --font "Arial" --body-size 12

# Fazer a engenharia reversa (docx -> markdown)
docxify extract document.docx

# Converter um diretório em lote
docxify batch ./markdown-files/ -o ./docx-output/

# Extrair um diretório em lote
docxify batch ./docx-files/ -o ./md-output/ --reverse
```

### 🧠 Workflow Prático (Workflow de Automação IA)

1. Copie o texto (ou force a saída do seu Agente favorito via tool call) em Markdown.
2. Salve o arquivo localmente em `.md`.
3. Rode `docxify convert response.md -o relatorio_final.docx`. As tabelas, negritos e marcações se tornarão elementos nativos de Microsoft Word sem "quebras" estranhas.

### 📄 Licença
Licença MIT. Livre para uso comercial e corporativo.

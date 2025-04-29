<p align="center">
  <picture>
    <img alt="TextPy" src="https://github.com/yezhengmao1/TextPy/tree/main/docs/logos/TextPy.png" width=55%>
  </picture>
</p>

<p align="center">
| <a href="https://github.com/yezhengmao1/TextPy"><b>Documentation</b></a> | <a href="https://github.com/yezhengmao1/TextPy"><b>Blog</b></a> | <a href="https://github.com/yezhengmao1/TextPy"><b>Paper</b></a> |
</p>

# TextPy ── Agentic Ability in One Line


### 🚀 Core Philosophy
**Code as Natural Language Manifestation**  

```
Function Definition = Specification = Implementation
```

### ✨ Magical Syntax
```python
from textpy import code, text


@text
def analyze_sentiment(*, text: str) -> dict[str, float]: ...

@code
def extract_text_from_pdf(*, file_path: str) -> str: ...
```

### ✨ Direct execution:
```python
print(analyze_sentiment(text="This framework is mind-blowing!"))
text = extract_text_from_pdf("path/to/pdffile.pdf")
```

---

### ⚡ Revolutionary Features
- **Semantic Transpiler**: Function signatures as natural language directives
- **Zero-Shot Programming**: Generate reliable code without examples
- **Hybrid Execution**: Seamlessly blend LLM-generated code with legacy systems
- **Self-Bootstrapping**: Extend framework using its own @text/@code decorators

---

### 🛠️ Quick Start

```python
from textpy import code, text


@text
def generate_poem(*, theme: str, style: str) -> str: ...


@code
# text should in center of the SVG
# use a white background
# add visually striking elements
def create_svg_from_text_with_svgwrite(*, text: str) -> str: ...


@code
def save_svg_to_file(*, svg: str, path: str): ...


poem = generate_poem(theme="Quantum Physics and Romance", style="haiku")

svg = create_svg_from_text_with_svgwrite(text=poem)

save_svg_to_file(svg=svg, path="poem.svg")
```
```bash
uv pip install -e .
python demo.py
```
---

---

### 📌 Join the Revolution
```bash
git clone https://github.com/yezhengmao1/TextPy
```


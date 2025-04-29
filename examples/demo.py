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

import logging
import sys

from rich.logging import RichHandler
from rich.pretty import pprint

from textpy import AICompiler, code, text

AICompiler.set_compiler(cache="/cache")

logger_module = ["CodeFunc", "TextFunc", "OptimizeCode", "PyEngine"]
for mo in logger_module:
    logging.getLogger(mo).setLevel(logging.INFO)
    logging.getLogger(mo).addHandler(RichHandler())


@text(cache="/cache")
def extract_id_from_url_for_filename(*, url: str) -> str: ...


@code(
    cache="/cache",
    pypi_package=[
        "https://raw.githubusercontent.com/lukasschwab/arxiv.py/refs/heads/master/README.md",
    ],
)
def download_pdf_from_arxiv(*, id: str, dir: str, file_name: str): ...


@code(cache="/cache")
# use ocrmypdf and PyPDF2 to extract text
def extract_text_from_pdf(*, dir: str, file_name: str) -> str: ...


@code(cache="/cache")
# ignore the case sensitivity of "references"
def extract_text_before_and_after_references(*, text: str) -> tuple[str, str]: ...


@text(cache="/cache")
def extract_reference_list_from_references_section(*, text: str) -> list[str]: ...


if __name__ == "__main__":
    assert len(sys.argv) >= 3

    arxiv_id = sys.argv[1]
    path = sys.argv[2]

    download_pdf_from_arxiv(id=arxiv_id, dir=path, file_name=arxiv_id)

    text = extract_text_from_pdf(dir=path, file_name=arxiv_id)

    pprint(text)

    before_ref, after_ref = extract_text_before_and_after_references(text=text)

    reference_list = extract_reference_list_from_references_section(text=after_ref)

    pprint(before_ref)

    pprint(reference_list)

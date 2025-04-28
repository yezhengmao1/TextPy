import logging
import sys

from rich.logging import RichHandler

from textpy import AICompiler, code, text

AICompiler.set_compiler(cache="/cache")

logger_module = ["CodeFunc", "TextFunc", "OptimizeCode", "PyEngine"]
for mo in logger_module:
    logging.getLogger(mo).setLevel(logging.INFO)
    logging.getLogger(mo).addHandler(RichHandler())


@text(cache="/cache")
def extract_id_from_url_for_filename(*, url: str) -> str: ...


@code(cache="/cache")
def download_pdf_from_arxiv(*, url: str, dir: str, file_name: str): ...


@code(cache="/cache")
# use ocrmypdf and PyPDF2 to extract text
def extract_text_from_pdf(*, dir: str, file_name: str) -> str: ...


if __name__ == "__main__":
    assert len(sys.argv) >= 3

    url = sys.argv[1]
    path = sys.argv[2]

    file_name = extract_id_from_url_for_filename(url=url)
    download_pdf_from_arxiv(url=url, dir=path, file_name=file_name)

    text = extract_text_from_pdf(dir=path, file_name=file_name)

    print(text)

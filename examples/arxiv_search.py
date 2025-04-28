import logging
import sys

from rich.logging import RichHandler

from textpy import AICompiler, code, text

AICompiler.set_compiler(cache="/cache")

logger_module = ["CodeFunc", "TextFunc", "OptimizeCode"]
for mo in logger_module:
    handler = RichHandler()
    handler.setFormatter(
        logging.Formatter("[%(name)s][%(levelname)s][%(asctime)s]:%(message)s")
    )
    logging.getLogger(mo).setLevel(logging.INFO)
    logging.getLogger(mo).addHandler()


@text(cache="/cache")
def extract_id_from_url_for_filename(*, url: str) -> str: ...


@code(cache="/cache")
def download_pdf_from_arxiv(*, url: str, dir: str, file_name: str): ...


if __name__ == "__main__":
    assert len(sys.argv) >= 3

    url = sys.argv[1]
    path = sys.argv[2]

    download_pdf_from_arxiv(
        url=url, dir=path, file_name=extract_id_from_url_for_filename(url=url)
    )

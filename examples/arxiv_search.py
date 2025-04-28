import sys

from textpy import code


@code
def download_pdf_from_arxiv(*, url: str, path: str): ...


if __name__ == "__main__":
    assert len(sys.argv) >= 3

    url = sys.argv[1]
    path = sys.argv[2]

    download_pdf_from_arxiv(url=url, path=path)

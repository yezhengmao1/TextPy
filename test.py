from textpy import code


@code
# curl pdf from url, and summary the pdf
def curl_from_arxiv_and_summary(*, url: str) -> str: ...


if __name__ == "__main__":
    curl_from_arxiv_and_summary(url="https://arxiv.org/pdf/2310.03714")

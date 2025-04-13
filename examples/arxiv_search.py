import concurrent.futures
import logging
import sys
import threading

from textpy import code, text

logger = logging.getLogger("ArxivSearch")

ARXIV_ID = sys.argv[1]
CACHE_DIR = sys.argv[2]
SEARCH_DEPTH = int(sys.argv[3])

ARXIV_PAPER_DIR = CACHE_DIR + "/arxiv"
HTML_PATHNAME = CACHE_DIR + "/arxiv.html"


g_tp_executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)


def get_arxiv_package_info() -> str:
    import requests

    url = "https://raw.githubusercontent.com/lukasschwab/arxiv.py/refs/heads/master/README.md"

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""


@code(cache=CACHE_DIR)
# the url is like https://arxiv.org/abs/2301.00001
# or https://arxiv.org/pdf/2301.00001v2
def extract_id_from_arxiv_entry_id(*, url: str) -> str: ...


@code(cache=CACHE_DIR, pypi_package=[get_arxiv_package_info()])
def download_pdf_from_arxiv(*, id: str, dir: str, file_name: str): ...


@code(cache=CACHE_DIR, pypi_package=[get_arxiv_package_info()])
# return only one title for this paper, if do not exist return None
def search_this_arxiv_id_title(*, id: str): ...


@code(cache=CACHE_DIR)
# use ocrmypdf and PyPDF2 to extract text
def extract_text_from_pdf(*, dir: str, file_name: str) -> str: ...


@code(cache=CACHE_DIR)
# ignore the case sensitivity of "references"
def extract_text_before_and_after_references(*, text: str) -> tuple[str, str]: ...


@code(cache=CACHE_DIR, pypi_package=[get_arxiv_package_info()])
def search_arxiv_paper_from_query(*, query: str, max_result: int = 1) -> list: ...


@text(cache=CACHE_DIR)
# only need the title
def extract_reference_list_from_references_section(*, text: str) -> list[str]: ...


@text(cache=CACHE_DIR)
def summary_the_paper_by_sections(*, text: str) -> str: ...


@code(cache=CACHE_DIR)
# nodes is dict, key is arxiv_id, value is {"title": "..", "summary": "..."}
# edges is dict, key is arxiv_id, value is child arxiv_ids(list)
# generate the graph structure, each node include title and summary(markdown format)
# do not omit the summary, correct render the markdown format text
# also the summary in the html can be collapsed
# the html file is utf-8 code
def generate_html_from_graph_structure(*, nodes: dict, edges: dict) -> str: ...


@code(cache=CACHE_DIR)
def save_html_file(*, text: str, path: str): ...


@code(cache=CACHE_DIR)
# create a new thread to start http server listen the port
# and serve all file in the dir
# support utf-8
def start_http_server(*, port: int, dir: str): ...


locker = threading.Lock()
visited_papers = {}
paper_refs_relationship = {}


def record_paper_title_and_summary(arxiv_id: str, title: str, summary: str):
    global visited_papers
    global locker
    with locker:
        visited_papers[arxiv_id] = {"title": title, "summary": summary}


def record_paper_relationship(father_id: str, arxiv_id: str):
    global paper_refs_relationship
    global locker

    with locker:
        if father_id not in paper_refs_relationship:
            paper_refs_relationship[father_id] = []

        paper_refs_relationship[father_id].append(arxiv_id)


def deep_read_arxiv_paper(father_id: str, arxiv_id: str, dir_path: str, depth: int):
    """
    Download the paper from arxiv and extract the text from the pdf
    """
    if depth >= SEARCH_DEPTH:
        return

    paper_title = search_this_arxiv_id_title(id=arxiv_id)
    logger.info(f"get paper title {arxiv_id} done: {paper_title[:70]}")

    download_pdf_from_arxiv(id=arxiv_id, dir=dir_path, file_name=arxiv_id)
    logger.info(f"download pdf - {arxiv_id} done.")

    text = extract_text_from_pdf(dir=dir_path, file_name=arxiv_id)
    before_ref, after_ref = extract_text_before_and_after_references(text=text)
    logging.info(f"extract text from pdf - {arxiv_id} done.")

    paper_summary = summary_the_paper_by_sections(text=before_ref)
    logging.info(f"summary text {arxiv_id} done: {paper_summary[:70]}")

    record_paper_title_and_summary(
        arxiv_id=arxiv_id, title=paper_title, summary=paper_summary
    )

    reference_list = extract_reference_list_from_references_section(text=after_ref)
    logging.info(f"get references from {arxiv_id} done.")

    record_paper_relationship(father_id=father_id, arxiv_id=arxiv_id)

    html_text = generate_html_from_graph_structure(
        nodes=visited_papers, edges=paper_refs_relationship
    )
    save_html_file(text=html_text, path=HTML_PATHNAME)
    logging.info(f"save html file - {arxiv_id} done.")

    for reference_title in reference_list:
        result = search_arxiv_paper_from_query(
            query='ti:"' + reference_title + '"', max_result=1
        )
        if len(result) <= 0:
            continue

        ref_paper = result[0]
        ref_paper_id = extract_id_from_arxiv_entry_id(url=ref_paper["entry_id"])

        if ref_paper_id in visited_papers:
            continue

        g_tp_executor.submit(
            deep_read_arxiv_paper,
            father_id=arxiv_id,
            arxiv_id=ref_paper_id,
            dir_path=dir_path,
            depth=depth + 1,
        )


if __name__ == "__main__":
    assert len(sys.argv) >= 3

    for logger_name in ["CodeFunc", "TextFunc", "ArxivSearch"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s]: %(message)s")
        )

        logger.addHandler(handler)

    start_http_server(port=31108, dir=CACHE_DIR)
    logger.info("start html server done.")

    record_paper_title_and_summary(arxiv_id="root", title="root", summary="root")
    deep_read_arxiv_paper(
        father_id="root", arxiv_id=ARXIV_ID, dir_path=ARXIV_PAPER_DIR, depth=0
    )

    g_tp_executor.shutdown(wait=True)

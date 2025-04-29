import concurrent.futures
import logging
import sys
import threading

from textpy import AICompiler, code, text

logger = logging.getLogger("ArxivSearch")

ARXIV_ID = sys.argv[1]
CACHE_DIR = sys.argv[2]
SEARCH_DEPTH = int(sys.argv[3])

ARXIV_PAPER_DIR = CACHE_DIR + "/arxiv"
COMPILER_CACHE = CACHE_DIR + "/prompts"
HTML_PATHNAME = CACHE_DIR + "/arxiv.html"
SQLITE_DIR = CACHE_DIR + "/store.db3"

AICompiler.set_compiler(cache=COMPILER_CACHE)

g_tp_executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)


def get_arxiv_package_info() -> str:
    import requests

    url = "https://gist.yezhem.com/yezhengmao/0e01a14b27084d7387eaac9ecd1f2036/raw/HEAD/readme.md"

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""


@code(cache=COMPILER_CACHE)
# the url is like https://arxiv.org/abs/2301.00001
# or https://arxiv.org/pdf/2301.00001v2
def extract_id_from_arxiv_entry_id(*, url: str) -> str: ...


@code(cache=COMPILER_CACHE, pypi_package=[get_arxiv_package_info()])
def download_pdf_from_arxiv(*, id: str, dir: str, file_name: str): ...


@code(cache=COMPILER_CACHE, pypi_package=[get_arxiv_package_info()])
# return only one title for this paper, if do not exist return None
def search_this_arxiv_id_title(*, id: str): ...


@code(cache=COMPILER_CACHE)
# use ocrmypdf and PyPDF2 to extract text
def extract_text_from_pdf(*, dir: str, file_name: str) -> str: ...


@code(cache=COMPILER_CACHE)
# ignore the case sensitivity of "references"
def extract_text_before_and_after_references(*, text: str) -> tuple[str, str]: ...


@code(cache=COMPILER_CACHE, pypi_package=[get_arxiv_package_info()])
def search_arxiv_paper_from_query(*, query: str, max_result: int = 1) -> list: ...


@text(cache=COMPILER_CACHE)
# only need the title
def extract_reference_list_from_references_section(*, text: str) -> list[str]: ...


@text(cache=COMPILER_CACHE)
def summary_the_paper_by_sections(*, text: str) -> str: ...


@code(cache=COMPILER_CACHE)
# nodes is dict, key is arxiv_id, value is {"title": "..", "summary": "..."}
# edges is dict, key is arxiv_id, value is child arxiv_ids(list)
# generate the graph structure, each node include title and summary(markdown format)
# do not omit the summary, correct render the markdown format text
# also the summary in the html can be collapsed
def generate_html_from_graph_structure(*, nodes: dict, edges: dict) -> str: ...


@code(cache=COMPILER_CACHE)
def save_html_file(*, text: str, path: str): ...


@code(cache=COMPILER_CACHE)
# write the sqlite database, table like
# CREATE TABLE IF NOT EXISTS papers (
#     arxiv_id TEXT PRIMARY KEY,
#     title TEXT,
#     summary TEXT
# );
def write_arxiv_paper_summary_to_db(
    *, db_path: str, arxiv_id: str, title: str, paper_summary: str
): ...


@code(cache=COMPILER_CACHE)
# read from sqlite database table like
# CREATE TABLE IF NOT EXISTS papers (
#     arxiv_id TEXT PRIMARY KEY,
#     title TEXT,
#     summary TEXT
# );
# if arxiv_id not exist return None,None
# else return title(str), summary(str)
def read_arxiv_paper_title_and_summary(*, db_path: str, arxiv_id: str): ...


@code(cache=COMPILER_CACHE)
# write the sqlite database table like
# CREATE TABLE IF NOT EXISTS paper_references (
#     arxiv_id TEXT,
#     reference_title TEXT,
#     PRIMARY KEY (arxiv_id, reference_title)
# );
def write_paper_all_reference_title_to_db(
    *, db_path: str, arxiv_id: str, reference_titles: list[str]
): ...


@code(cache=COMPILER_CACHE)
# read from sqlite databse table like
# CREATE TABLE IF NOT EXISTS paper_references (
#     arxiv_id TEXT,
#     reference_title TEXT,
#     PRIMARY KEY (arxiv_id, reference_title)
# );
# if arxiv_id not exist return None else return list[str]
def read_paper_all_reference_title_from_db(*, db_path: str, arxiv_id: str): ...


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

    paper_title, paper_summary = read_arxiv_paper_title_and_summary(
        db_path=SQLITE_DIR, arxiv_id=arxiv_id
    )

    if paper_summary is None:
        paper_title = search_this_arxiv_id_title(id=arxiv_id)
        logger.info(f"get paper title {arxiv_id} done: {paper_title}")

        download_pdf_from_arxiv(id=arxiv_id, dir=dir_path, file_name=arxiv_id)
        logger.info(f"download pdf - {arxiv_id} done.")

        text = extract_text_from_pdf(dir=dir_path, file_name=arxiv_id)
        before_ref, after_ref = extract_text_before_and_after_references(text=text)
        logging.info(f"extract text from pdf - {arxiv_id} done.")

        paper_summary = summary_the_paper_by_sections(text=before_ref)
        logging.info(f"summary text {arxiv_id} done.")

        reference_list = extract_reference_list_from_references_section(text=after_ref)
        logging.info(f"get references from {arxiv_id} done.")

        write_arxiv_paper_summary_to_db(
            db_path=SQLITE_DIR,
            arxiv_id=arxiv_id,
            title=paper_title,
            paper_summary=paper_summary,
        )
        write_paper_all_reference_title_to_db(
            db_path=SQLITE_DIR, arxiv_id=arxiv_id, reference_titles=reference_list
        )
    else:
        reference_list = read_paper_all_reference_title_from_db(
            db_path=SQLITE_DIR, arxiv_id=arxiv_id
        )

    record_paper_title_and_summary(
        arxiv_id=arxiv_id, title=paper_title, summary=paper_summary
    )
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

    record_paper_title_and_summary(arxiv_id="root", title="root", summary="root")
    deep_read_arxiv_paper(
        father_id="root", arxiv_id=ARXIV_ID, dir_path=ARXIV_PAPER_DIR, depth=0
    )

    g_tp_executor.shutdown(wait=True)

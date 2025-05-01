import concurrent.futures
import logging

from textpy import code, text

logger = logging.getLogger("DailyArxiv")

ARXIV_URL = "https://rss.arxiv.org/rss/cs.ai+cs.ce+cs.db+cs.dc+cs.ma+cs.os+cs.sy"
DB_PATH = "./store.db"
MD_PATH = "./daily_arxiv.md"


@code
def get_the_rss_xml_file_str(*, url: str) -> str: ...


@code(pypi=[get_the_rss_xml_file_str(url=ARXIV_URL)])
# return list[dict], the dict like {"title"="","link"="","abstract"=""}
def get_all_item_in_the_rss_file(*, xml_file_str: str) -> list[dict]: ...


@text
# only translate the abstrct, no other output
def translate_the_en_abstract_to_zh(*, abstract: str) -> str: ...


@code
# the sqlite3 table like below, if the table not exist create it.
# create table articles (
#     link text primary key,
#     title text,
#     abstract text,
#     zh_abstract text
# );
def check_link_in_db(*, db_path: str, link: str) -> bool: ...


@code
# the sqlite3 table like below, if the table not exist create it.
# create table articles (
#     link text primary key,
#     title text,
#     abstract text,
#     zh_abstract text
# );
# item is dict, {"title"="","link"="","abstract"="", "zh_abstract"=""}
def save_article_to_db(*, db_path: str, item: dict): ...


@code
# write the dict to the markdown file, transfer the dict to markdown format
# items is list[dict], the item is {"title"="","link"="","abstract"="", "zh_abstract"=""}
def write_to_markdown_file(*, file_path: str, items: list[dict]): ...


@text
# according the papers abstract to check if the topic is satisfactory
def check_topic_is_satisfactory(*, abstrct: str, topic: str) -> bool: ...


def process_item(item: dict):
    logger.info(f'processing item: {item["title"]} ...')

    if check_link_in_db(db_path=DB_PATH, link=item["link"]):
        logger.info(f'processing item: {item["title"]} already in db.')
        return None

    ret_item = None
    check = check_topic_is_satisfactory(
        abstract=item["abstract"],
        topic="(large language model) OR (DL training system AND DL inference system)",
    )

    assert isinstance(check, bool)

    if not check:
        logger.info(f'not satisfy the topic: {item["title"]} .')
        item["zh_abstract"] = ""
        ret_item = None
    else:
        item["zh_abstract"] = translate_the_en_abstract_to_zh(abstract=item["abstract"])
        ret_item = item

    save_article_to_db(db_path=DB_PATH, item=item)

    logger.info(f'processing item: {item["title"]} done.')

    return ret_item


def daily_arxiv():
    xml_file_str = get_the_rss_xml_file_str(url=ARXIV_URL)
    items = get_all_item_in_the_rss_file(xml_file_str=xml_file_str)
    logger.info(f"need to process {len(items)}")
    item_results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_item = {executor.submit(process_item, item): item for item in items}

        for future in concurrent.futures.as_completed(future_to_item):
            try:
                result = future.result()
                if result is not None:
                    item_results.append(result)
            except Exception as e:
                logger.error(f"error processing item: {e}")

    write_to_markdown_file(file_path=MD_PATH, items=item_results)


if __name__ == "__main__":

    for logger_name in ["CodeFunc", "TextFunc", "DailyArxiv"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s]: %(message)s")
        )

        logger.addHandler(handler)

    daily_arxiv()


import json
import os
from os import makedirs
from os.path import exists

import requests
import logging
from requests.sessions import Session

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

INDEX_URL = "https://**************************offset={offset}&limit={limit}"
COOKIE = r"_ga=GA***********************************************************jango_language=zh"

LIMIT = 10

RESULTS_DIR = "results"
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def get_count(data):

    count = data.get("data").get("count")
    logging.info(f"There are {count} comments now.")

    return count


def save_all(data, name):

    data_path = f"{RESULTS_DIR}/{name}_all.json"
    json.dump(
        data, open(data_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2
    )


def save_comments(data, name):

    data_path = f"{RESULTS_DIR}/{name}.json"
    data_to_dump = {}

    for page in data:
        page_data = data.get(page)
        userlist = page_data.get("data").get("results")

        for user in userlist:
            name = user.get("user_info").get("name")
            text = user.get("content").get("text")

            if data_to_dump.get(name, 0) == 0:
                data_to_dump[name] = [text]
            elif text not in data_to_dump[name]:
                data_to_dump[name].append(text)

    json.dump(
        data_to_dump,
        open(data_path, "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=2,
    )

    logging.info(f"Comments saved in: {data_path}")
    return data_path


def save_comments_txt(data_path):
    with open(data_path, "rb") as f:
        comments = json.load(f)

    txt_name = data_path.split(".")[0] + ".txt"
    with open(txt_name, "w", encoding="utf-8") as f:
        for (k, v) in comments.items():
            for text in v:
                f.write(text + "\n")

    logging.info(f"Comments of pure txt saved in: {txt_name}")


def scrape_api(url):

    logging.info("scraping %s...", url)

    session = Session()
    session.headers.update(
        {
            "Cookie": COOKIE,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        }
    )

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error(
            "get invalid status code %s while scraping %s", response.status_code, url
        )
    except requests.RequestException:
        logging.error("error occurred while scraping %s", url, exc_info=True)


def scrape_index():

    record = 0
    data_all_pages = {}

    url = INDEX_URL.format(limit=LIMIT, offset=0)
    data_all_pages[0] = scrape_api(url)

    pages = get_count(data_all_pages[0]) // LIMIT
    logging.info(f"There are {pages} pages")

    for page in range(1, pages):
        url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
        data_all_pages[page] = scrape_api(url)

    return data_all_pages


if __name__ == "__main__":

    data_all_pages = scrape_index()

    # # Only for debugging usage
    # save_all(data_all_pages)
    # with open("results/all_data.json", "rb") as f:
    #     data_all_pages = json.load(f)

    # BookName = "活出生命的意义"
    BookName="天资差异"
    data_path = save_comments(data_all_pages, BookName)
    save_comments_txt(data_path)

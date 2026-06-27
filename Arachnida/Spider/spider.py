# imports
import sys
import requests
from bs4 import BeautifulSoup
from parsing import parse_argv, make_dir, Params
from images import get_img, Stats
from links import get_links
from urllib.parse import urlparse


# config
HEADERS = {'user-agent': 'spider42/0.1'}
PATH = "./data/"
USAGE = "Usage: spider.py [-r] [-r -l LEVEL] [-p PATH] URL"
TIMEOUT = 5


# functions
def get_soup(url: str, headers: dict[str, str], timeout: int) -> BeautifulSoup | None:
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()  # 404 403 500
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None


def crawl(links: set, params: Params, level: int, visited: set[str], stats: Stats) -> None:
    if level > params.level:
        return
    for url in links:
        short_url = urlparse(url)._replace(fragment="").geturl()
        if short_url not in visited:
            visited.add(short_url)
            print(f"\nvisiting {url}")
            soup = get_soup(url, HEADERS, TIMEOUT)
            if soup is None:
                continue
            get_img(url, params.path, HEADERS, TIMEOUT, stats, soup)
            newlinks = get_links(url, soup)
            crawl(newlinks, params, level + 1, visited, stats)


# main
def main() -> None:
    try:
        params = parse_argv(sys.argv, USAGE, PATH)
        make_dir(params.path, PATH)
        visited = set()
        stats = Stats(n_img=0)
        init_level = 0
        crawl({params.url}, params, init_level, visited, stats)
        print(f"\nTotal saved: {stats.n_img} images")
    except KeyboardInterrupt:
        print("\nSpider interrupted by user")


if __name__ == "__main__":
    main()

# import
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


# functions
def check_link(url: str, link: str) -> bool:
    if link.startswith("http://") or link.startswith("https://"):
        if urlparse(url).netloc == urlparse(link).netloc:
            return True
    return False


def get_links(url: str, soup: BeautifulSoup) -> set[str]:
    links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if href is None or href == "":
            continue
        newlink = urljoin(url, href)
        if check_link(url, newlink):
            links.add(newlink)
    return links

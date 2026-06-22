# import
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


# functions
def check_link(url: str, link:str) -> bool:    
    if link.startswith("http://") or link.startswith("https://"):        
        if urlparse(url).netloc == urlparse(link).netloc:
            return(True)
    return(False)    


def get_links(url: str, headers: dict[str,str], timeout: int) -> set:
    links = set()
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status() # 404 403 500
        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('a'):
            # print(link.get('href'))
            newlink = urljoin(url, link.get('href'))
            # print(newlink)
            if check_link(url, newlink):
                links.add(newlink)
        return(links)
    except requests.exceptions.RequestException as e:
        # print(f"Request Error: {e}")
        return(links)

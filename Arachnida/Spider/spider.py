# ./spider [-rlp] URL
# Option -r : recursively downloads the images in a URL received as a parameter.
# Option -r -l [N] : indicates the maximum depth level of the recursive download.
#   If not indicated, it will be 5.
# Option -p [PATH] : indicates the path where the downloaded files will be saved.
#   If not specified, ./data/ will be used


# imports
import sys
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, urljoin
from parsing import parse_argv, make_dir


# config
HEADERS = {'user-agent': 'spider42/0.1'}
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]
PATH = "./data/"
USAGE = "Usage: spider.py [-r] [-r -l LEVEL] [-p PATH] URL"
TIMEOUT = 5


# functions    
def is_img(type: str) -> bool:
    for ext in EXTS:
        if type.startswith("image/" + ext):
            return(True)
    return(False)


def save_img(link: str, path: str, img: bytes) -> bool:
    filename = Path(urlparse(link).path).name
    p = Path(path) / filename # "/" operator of object Path()
    try:
        with p.open("wb") as f: # wb overwrite silently, xb raise FileExistsError if needed
            f.write(img)
            print(f"{p} saved")
            return(True)    
    except OSError as e:
        print(f"{p} not saved: {e}")
    return(False)   


def get_img(url: str, path: str, headers: dict[str,str], timeout: int) -> int:
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status() # 404 403 500
        soup = BeautifulSoup(r.text, 'html.parser')
        n = 0
        for img in soup.find_all('img'): # only img tag
            src = img.get('src')
            if src is None or src == "":
                continue
            try:
                img_link = urljoin(url, src)
                rep = requests.get(img_link, headers=headers, timeout=timeout)
                rep.raise_for_status()
                # print(rep.status_code)        
                if is_img(rep.headers.get("Content-Type", "")) and n < 2: # #######to remove ###############3
                    if save_img(img_link, path, rep.content):
                        n = n + 1                
            except requests.exceptions.RequestException as e:
                print(f"Request Error: {e}")
        print(f"{n} images saved")
        return(n)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return(0)


def get_links(url: str, headers: dict[str,str], timeout: int) -> list:
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status() # 404 403 500
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for link in soup.find_all('a'):
            # print(link)        
            newlink = urljoin(url, link.get('href'))
            # print(newlink)
            # if check_link(newlink):
            links.append(newlink)
        return(links)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return(links)


# main
def main() -> None:    
    params = parse_argv(sys.argv, USAGE, PATH)    
    make_dir(params.path, PATH)
    n = 0
    r_links = [params.url]    
    visited = set()
    i = 0
    while i <= params.level:
        for url in links:
            if url not in visited:
                print(f"visiting {url}")
                n += get_img(url, params.path, HEADERS, TIMEOUT)    
                links = get_links(url, HEADERS, TIMEOUT)
                visited.add(url)

        i += 1
    print(f"{n} images saved")
    

if __name__ == "__main__":
    main()

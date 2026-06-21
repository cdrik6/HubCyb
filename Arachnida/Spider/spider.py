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
from dataclasses import dataclass


# config
HEADERS = {'user-agent': 'spider42/0.1'}
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]
PATH = "./data/"
USAGE = "Usage: spider.py [-r] [-r -l LEVEL] [-p PATH] URL"
TIMEOUT = 5


# class
@dataclass
class Params:
    recur: bool
    level: int
    path: str
    url: str


# functions
def is_valid_url(url: str) -> bool:    
    if url.startswith("http://") or url.startswith("https://"):        
        if urlparse(url).netloc:
            return(True)
    return(False)
    
def is_img(type: str) -> bool:
    for ext in EXTS:
        if type.startswith("image/" + ext):
            return(True)
    return(False)

def save_img(link: str, path: str, img: bytes) -> bool:
    filename = Path(urlparse(link).path).name
    p = Path(path) / filename # / operator of object Path()
    try:
        with p.open("wb") as f:
            f.write(img)
            print(f"{p} saved")
            return(True)
    except OSError as e:
        print(f"{p} not saved: {e}")
    return(False)   


def get_img(url: str, path: str, headers: dict[str,str], timeout: int) -> None:
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status() # 404 403 500
        soup = BeautifulSoup(r.text, 'html.parser')
        n = 0
        for img in soup.find_all('img'): # ###############background img via css
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
    except requests.exceptions.RequestException as e:
                print(f"Request Error: {e}")

def is_there_url(args: list[str]) -> int | None:
    idx = 0
    for i in range(1, len(args)):
        if is_valid_url(args[i]):
            if idx != 0:
                return(None) # too many url
            idx = i
    if idx != 0:
        return(idx)            
    return(None) # missing or not valid

def is_there_recur(args: list[str]) -> bool:
    for i in range(1, len(args)):        
        if args[i].startswith("-") and "r" in args[i]:
                return(True)
    return(False)

def make_dir(path: str, default_path: str) -> str:
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        print(f"Directory used is: {path}")
        return(path)
    except OSError as e:
        print(f"Make directory {path} failed: {e}")
        try:
            Path(default_path).mkdir(parents=True, exist_ok=True)
            print(f"Images will be saved in {default_path}")
            return(default_path)
        except OSError as e:
            print(f"Make default directory {default_path} failed: {e}")
            sys.exit(1)
        

# spider.py [-r] [-r -l LEVEL] [-p PATH]] URL
# [r, l, p, url] = [bool, int, str, str]
def parse_argv(args: list[str], usage: str, default_path: str) -> Params:
    
    if len(args) < 2 or len(args) > 7:
        print("Wrong number of arguments")
        print(usage)
        sys.exit(1)    

    url_idx = is_there_url(args)
    if url_idx is None:
        print("URL missing, duplicate or not valid")
        print (usage)
        print("Valid url: http[s]://netloc[/path?query#fragment]")
        sys.exit(1)
    url = args[url_idx]

    level = 0
    path = default_path
    recur = is_there_recur(args)
    if recur:
        level = 5
    
    i = 1
    # standard CLI design attaches values to their options.
    while i < len(args):        
        if args[i].startswith("-") and "p" in args[i]:
            if i == len(args) - 1 or i + 1 == url_idx:
                print("The PATH is missing")                
                print(usage)                
            else:
                path = str(args[i + 1])                
                i += 1        
            path = make_dir(path, default_path)
        if args[i].startswith("-") and "l" in args[i]:
            if not recur:
                print("-l option is valid only with the -r option")
                print(usage)
            elif i == len(args) - 1 or i + 1 == url_idx:
                print("The LEVEL is missing, 5 will be used")
                print(usage)
            else:    
                try:
                    level = int(args[i + 1])
                    if level < 0:
                        print("The LEVEL should be a positive integer, 5 will be used")
                        level = 5                        
                except ValueError as e:
                    print("The LEVEL should be an integer, 5 will be used")
                    print(usage)
        i += 1

    return(Params(recur=recur, level=level, path=path, url=url))


# main
def main() -> None:    
    params = parse_argv(sys.argv, USAGE, PATH)
    get_img(params.url, params.path, HEADERS, TIMEOUT)
    # duplicate filename
    # -foobar
    

if __name__ == "__main__":
    main()

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
PATH = "./data"
USAGE = "Usage: spider.py [-r] [-r -l LEVEL] [-p PATH]] URL"


# class
@dataclass
class Params:
    recur: bool = False
    level: int = 0
    path: str = PATH
    url: str


# functions
def is_valid_scheme(url: str) -> bool:    
    if url.startswith("http://") or url.startswith("https://"):        
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


def get_img(url: str, path: str) -> None:
    try:
        r = requests.get(url, headers=HEADERS)    
        soup = BeautifulSoup(r.text, 'html.parser')
        n = 0
        for img in soup.find_all('img'): # background img via css
            src = img.get('src')
            if src is None or src == "":
                continue
            try:
                img_link = urljoin(url, src)
                rep = requests.get(img_link, headers=HEADERS)
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
        if is_valid_scheme(args[i]):
            if idx != 0:
                return(None) # too many url
            idx = i
    if idx != 0:
        return(idx)            
    return(None)

def is_there_recur(args: list[str]) -> bool:
    for i in range(1, len(args)):
        if args[i] == "-r":
                return(True)
    return(False)

# spider.py [-r] [-r -l LEVEL] [-p PATH]] URL
# [r, l, p, url] = [bool, int, str, str]
def parse_argv(args: list[str]) -> Params:    
    level = 0
    path = PATH   

    url_idx = is_there_url(args)
    if url_idx is None:
        print("URL missing, too many or not valid")
        print (USAGE)
        print("Valid url: http[s]://netloc[/path?query#fragment]")
        sys.exit(1)
    url = args[url_idx]

    recur = is_there_recur(args)
    if recur:
        level = 5

    i = 1
    while i < len(args):
        
        if args[i] == "-p":
            if i == len(args) - 1 or i + 1 == url_idx:
                print("The PATH is missing")
                print(USAGE)
            else:
                path = str(args[i + 1])
                # path = check_path(path) # ############to do ################
                i += 1
        
        if args[i] == "-l":
            if not recur:
                print("-l option is valid only with the -r option")
                print(USAGE)
            elif i == len(args) - 1 or i + 1 == url_idx:
                print("The LEVEL is missing")
                print(USAGE)
            else:    
                try:
                    level = int(args[i + 1])
                    if level < 0:
                        print("The LEVEL should be a positive integer")
                        level = 0
                except ValueError as e:
                    print("The LEVEL should be an integer")
                    print(USAGE)
    return(Params(recur=recur, level=level, path=path, url=url))


# main
def main() -> None:    
    if len(sys.argv) < 2 or len(sys.argv) > 7:
        print("Wrong number of arguments")
        print(USAGE)
        return
    params = parse_argv(sys.argv)

    try:
        Path(PATH).mkdir(exist_ok=True)    
    except OSError as e:
        print(f"Make directory failed: {e}")
    
    # url = scheme://netloc/path?query#fragment
    # netloc = hostname:port
    # netloc = urlparse(url).netloc
    # scheme = urlparse(url).scheme
    # url = params[3]
    if not is_valid_scheme(url):    
        print("AssertionError: url not valid")
        print("Valid url: http[s]://netloc[/path?query#fragment]")
        return
     
    get_img(params.url, params.path)
    
        
                
        

   
# https://villarson.com/portfolio.php

if __name__ == "__main__":
    main()

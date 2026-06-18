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

# config
HEADERS = {'user-agent': 'spider42/0.1'}
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]
PATH = "./data"


# class


# functions

def check_url(url: str) -> bool:
    # is_valid
    # can_fetch
    if url.startswith("http://") or url.startswith("https://"):
        try:
            rep = requests.get(url, headers=HEADERS)
            if rep.status_code == 200:
                return True
            else:
                print("AssertionError: connexion issue")
                return False    
        except Exception as e:        
            print("AssertionError:", e)
            return False
    else:
        print("AssertionError: wrong url")
        print("Valid url: http[s]://hostname/path")        
        return False    


# [r, l, p, url] = [bool, bool | int, str, bool | str]
def parse_argv(args: list) -> list:
    url = args[len(args) - 1]
    # if check_url(url) == False:
    #     return False
    # return url    
    return [False, False, PATH, url]

def link_abs(link:str) -> bool:
    rep = requests.get(link, headers=HEADERS)
    if rep.status_code == 200:
        for ext in EXTS:
            if rep.headers.get("Content-Type") == "image/" + ext:
                return True
    return False

def link_rel(url:str, link:str) -> bool:
    rep = requests.get(url + link, headers=HEADERS)
    if rep.status_code == 200:
        for ext in EXTS:
            if rep.headers.get("Content-Type") == "image/" + ext:
                return True
    return False

def is_valid(url:str, link: str) -> bool:
    if link_abs(link) or link_rel(url, link):
        return True
    return False

# main
def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 7:
        print("AssertionError: wrong number of arguments")
        print("Usage: spider.py [-r] [-r -l LEVEL] [-p PATH]] URL")        
        return    
    Path(PATH).mkdir(exist_ok=True)    
    url = parse_argv(sys.argv)[3]
    if check_url(url):
        pass
        # home = get_home(url)
    else:
        print("AssertionError: wrong url or connexion issue")
        print("Valid url: http[s]://hostname/path")
        return
    r = requests.get(url, headers=HEADERS)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.find_all('img'))
    for src in soup.find_all('img'): # background img via css
        # if is_valid(url, src.get('src')):
        print(src.get('src'))
        # print("https://villarson.com/" + src.get('src'))
        # rep = requests.get("https://villarson.com/" + src.get('src'), headers=HEADERS)
        # print(rep.status_code)        
        # print(rep.headers.get("Content-Type"))
        # print(rep.text[:3])
        # # https://villarson.com/portfolio.php//ptf/img/tot2.jpg
        # with open(PATH + "loopintro.jpg", "wb") as f:
        #     f.write(rep.content)
        #     # print(url + src.get('src'))

   
# https://villarson.com/portfolio.php

if __name__ == "__main__":
    main()

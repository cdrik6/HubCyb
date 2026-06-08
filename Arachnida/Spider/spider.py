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

# config
HEADERS = {'user-agent': 'spider42/0.1'}
EXTS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
PATH = "./data/"

# class

# functions
def check_url(url: str) -> bool:
    return True

# [r, l, p, url] = [bool, bool | int, str, bool | str]
def parse_argv(args: list) -> list:
    url = args[len(args) - 1]
    # if check_url(url) == False:
    #     return False
    # return url    
    return [False, False, PATH, url]

# main
def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 7:
        print("AssertionError: wrong number of arguments")
        print("Usage: spider.py [-r] [-r -l LEVEL] [-p PATH]] URL")        
        return
    url = parse_argv(sys.argv)[3]
    r = requests.get(url, headers=HEADERS)
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup)
    for src in soup.find_all('img'):        
        print("https://villarson.com/" + src.get('src'))
        rep = requests.get("https://villarson.com/" + src.get('src'), headers=HEADERS)
        print(rep.status_code)        
        print(rep.headers.get("Content-Type"))
        print(rep.text[:300])
        # https://villarson.com/portfolio.phpptf/img/tot2.jpg
        with open(PATH + "loopintro.jpg", "wb") as f:
            f.write(rep.content)
            # print(url + src.get('src'))

   


if __name__ == "__main__":
    main()

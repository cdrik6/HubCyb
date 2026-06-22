# ./spider [-rlp] URL
# Option -r : recursively downloads the images in a URL received as a parameter.
# Option -r -l [N] : indicates the maximum depth level of the recursive download.
#   If not indicated, it will be 5.
# Option -p [PATH] : indicates the path where the downloaded files will be saved.
#   If not specified, ./data/ will be used


# imports
import sys
from parsing import parse_argv, make_dir, Params
from images import get_img, Stats
from links import get_links


# config
HEADERS = {'user-agent': 'spider42/0.1'}
# EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]
PATH = "./data/"
USAGE = "Usage: spider.py [-r] [-r -l LEVEL] [-p PATH] URL"
TIMEOUT = 5


# functions
def crawl(links: set, params: Params, level: int, visited: set, stats: Stats) -> None:    
    # print(f"Level: {level}")
    if level > params.level:
        # print(f"Close level: {level}")
        return
    for url in links:
        if url not in visited:
            visited.add(url)
            # print(f"visiting {url} of level: {level}")            
            print(f"\nvisiting {url}")
            get_img(url, params.path, HEADERS, TIMEOUT, stats)    
            newlinks = get_links(url, HEADERS, TIMEOUT)
            crawl(newlinks, params, level + 1, visited, stats)


# main
def main() -> None:    
    params = parse_argv(sys.argv, USAGE, PATH)    
    make_dir(params.path, PATH)    
    visited = set()
    stats = Stats(n_img=0)
    crawl({params.url}, params, 0, visited, stats)
    print(f"\nTotal saved: {stats.n_img} images")
    

if __name__ == "__main__":
    main()

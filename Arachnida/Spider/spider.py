# ./spider [-rlp] URL
# Option -r : recursively downloads the images in a URL received as a parameter.
# Option -r -l [N] : indicates the maximum depth level of the recursive download.
#   If not indicated, it will be 5.
# Option -p [PATH] : indicates the path where the downloaded files will be saved.
#   If not specified, ./data/ will be used

# imports
import requests
import sys

# config
HEADERS = {'user-agent': 'spider42/0.1'}
EXTS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]

# class

# functions
def parse_argv(args: list):
    

# main
def main() -> None:
    if len(sys.argv) < 2 or len(sys.argv) > 7:
        print("AssertionError: wrong number of arguments")
        print("Usage: spider.py [-rl[N]p[PATH]] URL")
        return
    parse_argv(sys.argv)

if __name__ == "__main__":
    main()

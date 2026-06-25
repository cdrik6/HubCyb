# imports
import sys
from pathlib import Path
from urllib.parse import urlparse
from dataclasses import dataclass


# class
@dataclass
class Params:
    recur: bool
    level: int
    path: str
    url: str


def is_valid_url(url: str) -> bool:
    if url.startswith("http://") or url.startswith("https://"):
        if urlparse(url).netloc:
            return True
    return False


def is_there_url(args: list[str]) -> int | None:
    idx = 0
    for i in range(1, len(args)):
        if is_valid_url(args[i]):
            if idx != 0:
                return None  # too many url
            idx = i
    if idx != 0:
        return idx
    return None  # missing or not valid


def is_there_recur(args: list[str]) -> bool:
    for i in range(1, len(args)):
        # if args[i].startswith("-") and "r" in args[i]:
        if args[i] == "-r":
            return True
    return False


def check_tokens(args: list[str], url_idx: int) -> str | None:
    options = {"-r", "-l", "-p"}
    i = 1
    while i < len(args):
        if args[i].startswith("-") and args[i] not in options:
            return args[i]
        if args[i] not in options and i != url_idx:
            if args[i - 1] not in {"-l", "-p"}:
                return args[i]
        i += 1
    return None


def make_dir(path: str, default_path: str) -> str:
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        print(f"Directory used is: {path}")
        return path
    except OSError as e:
        print(f"Make directory {path} failed: {e}")
        try:
            Path(default_path).mkdir(parents=True, exist_ok=True)
            print(f"Images will be saved in {default_path}")
            return default_path
        except OSError as e:
            print(f"Make default directory {default_path} failed: {e}")
            sys.exit(1)


# spider.py [-r] [-r -l LEVEL] [-p PATH]] URL
# [r, l, p, url] = [bool, int, str, str]
def parse_argv(args: list[str], usage: str, default_path: str) -> Params:

    # number of arguments
    if len(args) < 2 or len(args) > 7:
        print("Wrong number of arguments")
        print(usage)
        sys.exit(1)

    # url
    url_idx = is_there_url(args)
    if url_idx is None:
        print("URL missing, duplicate or not valid")
        print(usage)
        print("Valid url: http[s]://netloc[/path?query#fragment]")
        sys.exit(1)
    url = args[url_idx]

    # invalid tokens
    invalid = check_tokens(args, url_idx) 
    if invalid is not None:
        print(f"Invalid arguments: {invalid}")
        print(usage)
        sys.exit(1)

    # default values
    level = 0
    path = default_path
    recur = is_there_recur(args)
    if recur:
        level = 5

    # options
    # standard CLI design attaches values to their options.
    i = 1
    while i < len(args):
        # if args[i].startswith("-") and "p" in args[i]:
        if args[i] == "-p":
            if i == len(args) - 1 or i + 1 == url_idx or args[i + 1] in {"-r", "-l", "-p"}:
                print("The PATH is missing")
                print(usage)            
            else:
                path = str(args[i + 1])
                i += 1
        # if args[i].startswith("-") and "l" in args[i]:
        if args[i] == "-l":
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
                except ValueError:
                    print("The LEVEL should be an integer, 5 will be used")
                    print(usage)
        i += 1

    return Params(recur=recur, level=level, path=path, url=url)

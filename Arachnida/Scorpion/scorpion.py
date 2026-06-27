# import
import sys
import argparse
from PIL import Image
from dataclasses import dataclass


# class
@dataclass
class Params:
    files: list[str]
    delete: bool
    modify: dict[str, str]


# config
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]
# USAGE = "Usage: scorpion.py FILE1 [FILE2 ...]"


# functions
def init_parser() -> Params:
    parser = argparse.ArgumentParser(
        description="Display, delete or modify image metadata"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="Image files"
    )
    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="Delete metadata of image files"
    )
    parser.add_argument(
        "-m",
        "--modify",
        action="append",
        metavar="KEY=VALUE",
        help="Modify metadata of image files"
    )
    args = parser.parse_args()    
    print(args)    
    print(args.delete)
    print(args.modify)    
    modify = {} # pass string from parser to dict of params
    if args.modify is not None:
        for m in args.modify:
            key, value = m.split("=", 1)
            modify[key] = value

    return Params(files=args.files, delete=args.delete, modify=modify)


# main
def main() -> None:
    try:
        params = init_parser()
        print(params)        
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

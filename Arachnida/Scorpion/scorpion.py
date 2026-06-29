# import
import sys
import argparse
from PIL import Image, ExifTags
from dataclasses import dataclass
from pathlib import Path


# class
@dataclass
class Params:
    files: list[str]
    delete: bool
    modify: dict[str, str]


# config
EXTS = ["jpg", "jpeg", "png", "gif", "bmp"]


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
    # print(args)    
    # print(args.delete)
    # print(args.modify)
    # print(type(args.modify))
    # from string of parser to dict of params
    modify = {} 
    if args.modify is not None:
        for m in args.modify:
            key, value = m.split("=", 1)
            modify[key] = value
    return Params(files=args.files, delete=args.delete, modify=modify)


def check_exts(format: str, exts: list[str]) -> bool:
    for ext in exts:
        if format == ext or format == ext.upper():
            return True
    return False


def print_exif(img: Image) -> None:
    # print(str(img.getexif()))
    print("\nEXIF")
    print("----")
    # if no exif #######################
    exif = img.getexif()
    for k, v in exif.items():
        print(f"{ExifTags.Base(k).name}: {v}")                        
    # gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
    # print(gps_ifd)


def print_attribut(img: Image, file: str) -> None:    
    p = Path(file)
    decor =""
    for i in range(len(p.name)):
        decor += "="
    print("\n" + decor)
    print(f"{p.name}")
    print(decor + "\n")
    print("Image")
    print("-----")
    print(f"Format: {img.format}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")    
    print(f"Stat: {p.stat().st_mtime}")
    # strftime("%b %d %Y")}\n")


def get_data(files: list[str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if check_exts(img.format, exts):
                    print_attribut(img, file)
                    print_exif(img)                    
                else:
                    print(f"Format not recognized: {file}")
        except OSError as e:
            print(f"Can't open {file}: {e}")


# main
def main() -> None:
    try:
        params = init_parser()
        # print(params)
        get_data(params.files, EXTS)
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

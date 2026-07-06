# import
import argparse
from dataclasses import dataclass
from metadata import get_data
from delete import delete_data
from modify import modify_data


# class
@dataclass
class Params:
    files: list[str]
    deldata: list[str]
    newdata: dict[str, str]


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
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-d",
        "--delete",
        action="append",
        metavar="Name",
        help="Delete ALL metadata (-d ALL), or only the specified EXIF Name"
    )
    group.add_argument(
        "-m",
        "--modify",
        action="append",
        metavar="Name=Value",
        help="Modify one or more EXIF Name"
    )
    args = parser.parse_args()

    # from string of parser to dict of params
    newdata = {}
    if args.modify is not None:
        for m in args.modify:
            key, value = m.split("=", 1)
            newdata[key] = value

    # from string of parser to list of params
    deldata = []
    if args.delete is not None:
        for name in args.delete:
            deldata.append(name)

    return Params(
        files=args.files,
        deldata=deldata,
        newdata=newdata
    )


# main
def main() -> None:
    try:
        params = init_parser()
        if params.deldata:
            delete_data(params.files, params.deldata, EXTS)
        elif params.newdata:
            modify_data(params.files, params.newdata, EXTS)
        else:
            get_data(params.files, EXTS)
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

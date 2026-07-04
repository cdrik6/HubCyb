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
    delete: bool
    deldata: list[str]
    modify: bool
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
        nargs="?",
        const="ALL",
        # nargs="*",        
        metavar="TAG",
        help="Delete all metadata, or only the specified EXIF tags"
    )
    group.add_argument(
        "-m",
        "--modify",
        action="append",
        metavar="KEY=VALUE",
        help="Modify one or more EXIF tags"
    )
    args = parser.parse_args()        
    
    # from string of parser to dict of params
    newdata = {}
    modify = False
    if args.modify is not None:
        modify = True
        for m in args.modify:
            key, value = m.split("=", 1)
            newdata[key] = value
    
    # from string of parser to list of params ################# ici avec le ALL *************
    deldata = []
    delete = False
    if args.delete is not None:
        delete = True
        for tag in args.delete:
            deldata.append(tag)
    return Params(
        files=args.files,
        delete=delete,
        deldata=deldata,
        modify=modify,
        newdata=newdata
    )


# main
def main() -> None:
    try:
        params = init_parser()
        if params.delete:
            delete_data(params.files, params.deldata, EXTS)
        elif params.modify:
            modify_data(params.files, params.newdata, EXTS)
        else:
            get_data(params.files, EXTS)
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

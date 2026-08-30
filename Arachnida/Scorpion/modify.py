import os
from PIL import Image, ExifTags
from metadata import check_exts
from pathlib import Path


# config
NAME_TO_TAG = {
    name: tag
    for tag, name in ExifTags.TAGS.items()
}


TAG_SCHEMA = {
    "Orientation": int,
    "ISOSpeedRatings": int,
    "Rating": int,
    "ResolutionUnit": int,
    # "XResolution": float, # IFDRational
    # "YResolution": float # IFDRational
}


def save_exif(img: Image.Image, file: str, exif: Image.Exif) -> bool:
    tmp = None
    try:
        # need to try to save a tmp file first to protect the original one in case of issue
        p = Path(file)
        # tmp = p.with_stem(p.stem + "_scorpion")
        tmp = p.with_name(f"{p.stem}_scorpion{p.suffix}")
        img.save(tmp, exif=exif)
        os.replace(tmp, file)
        print(f"Metadata of {file} modified")
        return True
    except Exception as e:
        if tmp is not None and tmp.exists():
            tmp.unlink()
        print(f"Can't save {file}: {e}")
        return False


def print_exif_tags() -> None:
    print("\nEXIF tags list:")
    for name in sorted(ExifTags.TAGS.values()):
        print(name)


def check_tag_type(tag_type: type, k: str, v: str) -> int | float | None:
    try:
        return tag_type(v)
    except ValueError:
        print(f"{k}: '{v}' is not a valid {tag_type.__name__}")
        return None


def set_data(img: Image.Image, file: str, data: dict[str, str]) -> None:
    exif = img.getexif()
    need_to_save = False
    print_tag_list = False
    for k, v in data.items():
        tag = NAME_TO_TAG.get(k)
        # print(type(exif[tag]))
        tag_type = TAG_SCHEMA.get(k)
        if tag is None:
            print(f"Unknown EXIF tag: {k}")
            print_tag_list = True
        elif tag_type is not None:
            v_typed = check_tag_type(tag_type, k, v)
            if v_typed is not None:
                exif[tag] = v_typed
                need_to_save = True
        else:
            exif[tag] = v
            need_to_save = True
    if need_to_save:
        save_exif(img, file, exif)
    if print_tag_list:
        print_exif_tags()


def modify_data(files: list[str], data: dict[str, str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                    return None
                if img.format.lower() == "gif" or img.format.lower() == "bmp":
                    print("Metadata modification is not supported for GIF/BMP images")
                else:
                    set_data(img, file, data)
        except OSError as e:
            print(f"Can't open {file}: {e}")

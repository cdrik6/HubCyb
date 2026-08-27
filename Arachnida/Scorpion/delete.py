from PIL import Image
from metadata import check_exts
from modify import save_exif, NAME_TO_TAG


def delete_name(exif: Image.Exif, img: Image.Image, file: str, data: list[str]) -> None:
    del_name = []
    for name in data:
        tag = NAME_TO_TAG.get(name)
        if tag is None:
            print(f"Unknown EXIF name: {name}")
        else:
            if exif.pop(tag, None) is not None:
                del_name.append(name)
    if len(del_name) == 0:
        print(f"Nothing to delete in {file}")
    else:
        if save_exif(img, file, exif):
            for name in del_name:
                print(f"{name} deleted in {file}")


def delete_exif(img: Image.Image, file: str, data: list[str]) -> None:
    print(f"\nEXIF state ({file})")
    print("----------")
    exif = img.getexif()
    if exif is None or len(exif) == 0:
        print("No EXIF metadata found, nothing to delete")
        return None

    if "ALL" in data:
        exif.clear()
        if save_exif(img, file, exif):
            print(f"Metadata of {file} deleted")
    else:
        delete_name(exif, img, file, data)


def delete_data(files: list[str], data: list[str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                else:
                    delete_exif(img, file, data)
        except OSError as e:
            print(f"Can't open {file}: {e}")

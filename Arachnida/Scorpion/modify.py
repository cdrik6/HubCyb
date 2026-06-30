import os
from PIL import Image, ExifTags
from metadata import check_exts
from pathlib import Path


# config
NAME_TO_TAG = {
    name: tag
    for tag, name in ExifTags.TAGS.items()
}


def set_data(img: Image.Image, file: str, data: dict[str, str]) -> None:
    exif = img.getexif()    
    need_to_save = False
    print_tag_list = False
    for k, v in data.items():
        tag = NAME_TO_TAG.get(k)
        if tag is None:
            print(f"Unknown EXIF tag: {k}")
            print_tag_list = True
        else:
            exif[tag] = v
            need_to_save = True
    if need_to_save:
        try:
            # need to try to save a tmp file first to protect the original one in case of issue
            p = Path(file)
            tmp = p.with_stem(p.stem + "_scorpion")
            img.save(tmp, exif=exif)
            os.replace(tmp, file)
            print(f"Metadata of {file} modified")
        except Exception as e:
            if tmp.exists():
                tmp.unlink()
            print(f"Can't save {file}: {e}")
    if print_tag_list:
        print("\nEXIF tags list:")
        for name in sorted(ExifTags.TAGS.values()):        
            print(name)
 

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

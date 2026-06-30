from PIL import Image, ExifTags
from pathlib import Path
from datetime import datetime


def check_exts(format: str, exts: list[str]) -> bool:    
    return format.lower() in exts


def print_exif(img: Image.Image) -> None:    
    print("\nEXIF")
    print("----")    
    exif = img.getexif()
    if exif is None or len(exif) == 0:
        print("No EXIF metadata found")
    for k, v in exif.items():
        tagname = ExifTags.TAGS.get(k, f"Unknown ({k})")
        print(f"{tagname}: {v}")  # {ExifTags.Base(k).name}


def print_attributes(img: Image.Image, file: str) -> None:    
    p = Path(file)    
    decor = "=" * len(p.name)
    print("\n" + decor)
    print(f"{p.name}")
    print(decor + "\n")
    print("Image")
    print("-----")
    print(f"Format: {img.format}")
    print(f"Size: {img.size}")
    print(f"Mode: {img.mode}")    
    print(
        f"File modification time: "
        f"{datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d %H:%M:%S}"
    )
    print(
        f"Filesystem change time: "
        f"{datetime.fromtimestamp(p.stat().st_ctime):%Y-%m-%d %H:%M:%S}"
    )    


def get_data(files: list[str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                else:    
                    print_attributes(img, file)
                    print_exif(img)
        except OSError as e:
            print(f"Can't open {file}: {e}")

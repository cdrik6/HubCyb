from PIL import Image, ExifTags
from metadata import check_exts

# config
NAME_TO_TAG = {
    name: tag
    for tag, name in ExifTags.TAGS.items()
}


def set_data(img: Image, file: str, data: dict[str, str]) -> None:
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
    if print_tag_list:
        print("EXIF tag list:")
        for t, name in ExifTags.TAGS.items():        
            print(f"{name}")
    if need_to_save:
        try:
            img.save(file, exif=exif)
            print(f"Metadata of {file} modified")
        except OSError as e:
            print(f"Can't save {file}: {e}")
 

def modify_data(files: list[str], data: dict[str, str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                else:    
                    set_data(img, file, data)
        except OSError as e:
            print(f"Can't open {file}: {e}")

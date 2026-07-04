from PIL import Image
from metadata import check_exts


def delete_exif(img: Image.Image, file: str, data: list[str]) -> None:
    print(data)
    print("\nEXIF state")
    print("----------")    
    exif = img.getexif()
    if exif is None or len(exif) == 0:
        print("No EXIF metadata found")
    else:
        if len(data) == 0:
            exif.clear()
            try:
                img.save(file, exif=exif)
                print(f"Metadata of {file} deleted")
            except OSError as e:
                print(f"Can't save {file}: {e}")
        else:            
            found_tag = []
            for tag in data:                
                for k in list(exif.keys()):
                    if tag == k:
                        # list() create a copy so no danger to loop and delete            
                        del exif[k]
                        found_tag.append(tag)                    
            if len(found_tag) == 0:
                print(f"Nothing to delete in {file}")
            else:
                try:
                    img.save(file, exif=exif)
                    for tag in found_tag:
                        print(f"{tag} deleted in {file}")
                except OSError as e:
                    print(f"Can't save {file}: {e}")


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

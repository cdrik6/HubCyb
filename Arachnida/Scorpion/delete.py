from PIL import Image
from metadata import check_exts

def delete_exif(img: Image.Image, file:str) -> None:    
    print("\nEXIF state")
    print("----------")    
    exif = img.getexif()
    if exif is None or len(exif) == 0:
        print("No EXIF metadata found")
    else:        
        for k in list(exif.keys()):
            # list() create a copy so no danger to loop and delete            
            del exif[k] # clear() or delete specific Tag #########################################3
        try:
            img.save(file, exif=exif)
            print(f"Metadata of {file} deleted")
        except OSError as e:
            print(f"Can't save {file}: {e}")


def delete_data(files: list[str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                else:
                    delete_exif(img, file)
        except OSError as e:
            print(f"Can't open {file}: {e}")

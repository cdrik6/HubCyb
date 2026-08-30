from PIL import Image
from metadata import check_exts
from modify import save_exif, NAME_TO_TAG
from tkinter import ttk


def clear_exif(tree: ttk.Treeview):
    attributes = ["Name", "Format", "Size", "Mode", "File modification time", "Filesystem change time",""]
    for item in tree.get_children():
        data_name = tree.item(item, "values")[0]
        if data_name not in attributes:
            tree.delete(item)


def delete_all(files: list[str], exts: list[str], tree: ttk.Treeview) -> None:
    if files[0] is None:
        return    
    delete_data(files, ["ALL"], exts, tree)


def delete_one(files: list[str], exts: list[str], tree: ttk.Treeview) -> None:
    if files[0] is None:
        return
    selection = tree.selection()
    # print(selection)
    if not selection:
        return
    values = []
    attributes = ["Name", "Format", "Size", "Mode", "File modification time", "Filesystem change time",""]
    for item in selection:        
        data_name = tree.item(item, "values")[0]
        if data_name not in attributes:
            values.append(data_name)
    # print(values)
    delete_data(files, values, exts, tree)
    for item in selection:
        data_name = tree.item(item, "values")[0]
        if data_name not in attributes:
            tree.delete(item)


def delete_name(exif: Image.Exif, img: Image.Image, file: str, data: list[str], tree: ttk.Treeview) -> None:
    del_name = []
    for name in data:
        tag = NAME_TO_TAG.get(name)
        if tag is None:            
            tree.insert("", "end", values=(name, "Unknown EXIF name"))
        else:            
            if exif.pop(tag, None) is not None:                
                del_name.append(name)                
    if len(del_name) == 0:        
        tree.insert("", "end", values=("Nothing to delete", ""))
    else:
        if save_exif(img, file, exif):
            for name in del_name:            
                tree.insert("", "end", values=(name, "deleted"))


def delete_exif(img: Image.Image, file: str, data: list[str], tree: ttk.Treeview) -> None:    
    exif = img.getexif()
    if exif is None or len(exif) == 0:
        tree.insert("", "end", values=("Nothing to delete", ""))
        return None
    if "ALL" in data:
        exif.clear()
        if save_exif(img, file, exif):
            clear_exif(tree)
            tree.insert("", "end", values=("Exif Metadata deleted", ""))
        else:
            tree.insert("", "end", values=("Can't delete metadata", ""))
    else:
        delete_name(exif, img, file, data, tree)


def delete_data(files: list[str], data: list[str], exts: list[str], tree: ttk.Treeview) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                else:
                    delete_exif(img, file, data, tree)
        except OSError as e:
            print(f"Can't open {file}: {e}")

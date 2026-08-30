import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ExifTags
from pathlib import Path
from datetime import datetime
from scorpion import EXTS


def check_exts(format: str, exts: list[str]) -> bool:
    return format.lower() in exts


def clear_tree(tree: ttk.Treeview):
    for item in tree.get_children():
        tree.delete(item)


def show_exif(img: Image.Image, tree: ttk.Treeview) -> None:    
    exif = img.getexif()    
    if exif is None or len(exif) == 0:
        tree.insert("", "end", values=("No EXIF metadata", ""))
        return None
    for k, v in exif.items():
        tagname = ExifTags.TAGS.get(k, f"Unknown ({k})")        
        tree.insert("", "end", values=(tagname, v))
    tree.insert("", "end", values=("", ""))


def show_attributes(img: Image.Image, file: str, tree: ttk.Treeview) -> None:
    p = Path(file)
    tree.insert("", "end", values=("Name", p.name))
    tree.insert("", "end", values=("Format", img.format))
    tree.insert("", "end", values=("Size", img.size))
    tree.insert("", "end", values=("Mode", img.mode))    
    tree.insert("", "end", values=("File modification time", 
        f"{datetime.fromtimestamp(p.stat().st_mtime):%Y-%m-%d %H:%M:%S}")
    )
    tree.insert("", "end", values=("Filesystem change time",
        f"{datetime.fromtimestamp(p.stat().st_ctime):%Y-%m-%d %H:%M:%S}")
    )
    tree.insert("", "end", values=("", ""))


def get_data(file: str, exts: list[str], tree: ttk.Treeview) -> None:    
    try:
        with Image.open(file) as img:
            if img.format is None or not check_exts(img.format, exts):
                print(f"Format not recognized: {file}")
            else:                
                show_attributes(img, file, tree)
                show_exif(img, tree)
    except OSError as e:
        print(f"Can't open {file}: {e}")


def get_photo(file: str, exts: list[str]) -> ImageTk.PhotoImage | None:
    try:
        with Image.open(file) as img:
            if img.format is None or not check_exts(img.format, exts):
                print(f"Format not recognized: {file}")
            else:                
                img.thumbnail((500, 500))
                photo = ImageTk.PhotoImage(img)                    
                return photo                
    except OSError as e:
        print(f"Can't open {file}: {e}")


def select_image(img_lbl: tk.Label, tree: ttk.Treeview, filename: list[str]):
    selected = filedialog.askopenfilename(
        title = "Select an image",
        filetypes = [
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )    
    if not selected:
        return
    filename[0] = selected
    clear_tree(tree)
    photo = get_photo(selected, EXTS)
    if photo is not None:
        img_lbl.config(image=photo, text="")
        img_lbl.image = photo         
        get_data(selected, EXTS, tree)        
    else:   
        img_lbl.config(image="", text="Unable to display this image")
        img_lbl.image = None    


def on_selected(tree: ttk.Treeview, name_entry: tk.Entry, value_entry:tk.Entry):
    selection = tree.selection()
    if not selection:
        return        
    values = tree.item(selection[0], "values")    
    name_entry.delete(0, tk.END)
    name_entry.insert(0, values[0])
    value_entry.delete(0, tk.END)
    value_entry.insert(0, values[1])

import tkinter as tk
from tkinter import filedialog, ttk
from scorpion import EXTS
from PIL import Image, ImageTk, ExifTags
from pathlib import Path
from datetime import datetime


def on_close(root):
    print("\nClosing Scorpion")
    root.destroy()


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


def show_attributes(img: Image.Image, file: str, tree: ttk.Treeview) -> None:
    p = Path(file)
    tree.insert("", "end", values=("Name", p.name))
    tree.insert("", "end", values=("Format", img.format))
    tree.insert("", "end", values=("Size", img.size))
    tree.insert("", "end", values=("Format", img.mode))    
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


def select_image(img_lbl: tk.Label, tree: ttk.Treeview):
    filename = filedialog.askopenfilename(
        title = "Select an image",
        filetypes = [
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )    
    if not filename:
        return
    clear_tree(tree)
    photo = get_photo(filename, EXTS)
    if photo is not None:
        img_lbl.config(image=photo, text="")
        img_lbl.image = photo         
        get_data(filename, EXTS, tree)
    else:   
        img_lbl.config(image="", text="Unable to display this image")
        img_lbl.image = None
    

def main():
    try:
        print("Opening Scorpion\n")
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
        root.title("Scorpion")
        root.geometry("600x800")

        open_frame = tk.Frame(root, borderwidth=2, relief="solid")
        open_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        image_frame = tk.Frame(root, borderwidth=2, relief="solid")
        image_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        data_frame = tk.Frame(root, borderwidth=2, relief="solid")
        data_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        button_frame = tk.Frame(root, borderwidth=2, relief="solid")
        button_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=0)
        root.rowconfigure(3, weight=1)       

        #
        img_lbl = tk.Label(image_frame, text="image preview")
        img_lbl.pack()

        #
        tree = ttk.Treeview(data_frame, columns=("name", "value"), show="headings")
        tree.heading("name", text="Metadata")
        tree.heading("value", text="Value")
        tree.column("name", width=250)
        tree.column("value", width=250)
        tree.pack(padx=10, pady=10)

        #
        lbl = tk.Label(open_frame, text="To get the metadata of an image, please open it here:")
        lbl.pack() #(expand=True)
        btn = tk.Button(open_frame, text="Open", command=lambda: select_image(img_lbl, tree))
        btn.pack(padx=10, pady=10)
        
        #        
        root.mainloop()
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

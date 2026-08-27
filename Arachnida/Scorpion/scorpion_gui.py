import tkinter as tk
from tkinter import filedialog, ttk
from scorpion import EXTS
from PIL import Image, ImageTk, ExifTags
from pathlib import Path
from datetime import datetime
from delete_gui import delete_all, delete_one
from modify_gui import modify


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
    tree.insert("", "end", values=("", ""))

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
        mod_frame = tk.Frame(root, borderwidth=2, relief="solid")
        mod_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        del_frame = tk.Frame(root, borderwidth=2, relief="solid")
        del_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=0)
        root.rowconfigure(3, weight=0)
        root.rowconfigure(4, weight=0)

        img_lbl = tk.Label(image_frame, text="image preview")
        img_lbl.pack()

        tree = ttk.Treeview(data_frame, columns=("name", "value"), show="headings")
        tree.heading("name", text="Metadata")
        tree.heading("value", text="Value")
        tree.column("name", width=250)
        tree.column("value", width=250)
        tree.pack(padx=10, pady=10)

        lbl = tk.Label(open_frame, text="To get the metadata of an image, please open it here:")
        lbl.pack() #(expand=True)
        filename = [None]
        btn = tk.Button(open_frame, text="Open", command=lambda: select_image(img_lbl, tree, filename))
        btn.pack(padx=10, pady=10)        

        name_line = tk.Frame(mod_frame)
        name_lbl = tk.Label(name_line, text="Name:")
        name_lbl.pack(side="left", padx=(0, 5))
        name_entry = tk.Entry(name_line)
        name_entry.pack(side="left")
        name_line.pack(padx=10, pady=10)
        value_line = tk.Frame(mod_frame)
        value_lbl = tk.Label(value_line, text="Value:")
        value_lbl.pack(side="left", padx=(0, 5))
        value_entry = tk.Entry(value_line)
        value_entry.pack(side="left")
        value_line.pack(padx=10, pady=10)
        btn_mod = tk.Button(mod_frame, text="Modify", command=lambda: modify(filename, EXTS, name_entry, value_entry, tree))
        btn_mod.pack(padx=10, pady=10)
        tree.bind("<<TreeviewSelect>>", lambda event: on_selected(tree, name_entry, value_entry))

        del_frame.rowconfigure(0, weight=1)
        del_frame.columnconfigure(0, weight=1)
        del_frame.columnconfigure(1, weight=1)
        btn_del = tk.Button(del_frame, text="Delete", command=lambda: delete_one(filename, EXTS, tree))
        btn_del.grid(row=0, column=0, padx=10, pady=10)
        btn_all = tk.Button(del_frame, text="Delete All", command=lambda: delete_all(filename, EXTS, tree))
        btn_all.grid(row=0, column=1, padx=10, pady=10)
                
        root.mainloop()
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

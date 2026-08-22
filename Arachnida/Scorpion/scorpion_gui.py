import tkinter as tk
from tkinter import filedialog, ttk
from scorpion import EXTS
from PIL import Image, ImageTk, ExifTags


def on_close(root):
    print("\nClosing Scorpion")
    root.destroy()


def check_exts(format: str, exts: list[str]) -> bool:
    return format.lower() in exts


def show_exif(img: Image.Image, tree: ttk.Treeview) -> None:
    # print("\nEXIF")
    # print("----")
    exif = img.getexif()
    if exif is None or len(exif) == 0:
        print("No EXIF metadata found")
        return None
    for k, v in exif.items():
        tagname = ExifTags.TAGS.get(k, f"Unknown ({k})")
        # print(f"{tagname}: {v}")
        tree.insert("", "end", values=(tagname, v))


def get_data(file: str, exts: list[str], tree: ttk.Treeview) -> None:    
    try:
        with Image.open(file) as img:
            if img.format is None or not check_exts(img.format, exts):
                print(f"Format not recognized: {file}")
            else:
                # print_attributes(img, file)
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
    photo = get_photo(filename, EXTS)
    if photo is not None:
        img_lbl.config(image=photo, text="")
        img_lbl.image = photo 
    else:   
        img_lbl.config(image="", text="Unable to display this image")
        img_lbl.image = None
    get_data(filename, EXTS, tree)

def main():
    try:
        print("Opening Scorpion\n")
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
        root.title("Scorpion")
        # root.geometry("1000x600")
        main_frame = tk.Frame(root, width=600, height=200, borderwidth=1, relief="solid")
        main_frame = tk.Frame(root)
        # main_frame.pack_propagate(False)
        main_frame.pack(padx=20, pady=20)

        main2_frame = tk.Frame(root, width=600, height=200, borderwidth=1, relief="solid")
        main2_frame = tk.Frame(root)
        # main_frame.pack_propagate(False)
        main2_frame.pack(padx=20, pady=20)

        # main_frame.columnconfigure(0, weight=1)
        # main_frame.columnconfigure(1, weight=1)
        # main_frame.rowconfigure(0, weight=1)
        # main_frame.rowconfigure(1, weight=1)

        # ******************
        open_frame = tk.Frame(main_frame, width=500, borderwidth=1, relief="solid")        
        open_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") #, columnspan=2)
        open_frame.grid_propagate(True)
        # ******************

        preview_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
        preview_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # metadata_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
        # metadata_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # 
        img_lbl = tk.Label(preview_frame, text="image preview")
        img_lbl.pack()
        # data_lbl = tk.Label(metadata_frame, text="metadata")
        # data_lbl.pack()

        # 
        tree = ttk.Treeview(root, columns=("name", "value"), show="headings")
        tree.heading("name", text="Metadata")
        tree.heading("value", text="Value")
        tree.column("name", width=250)
        tree.column("value", width=250)
        tree.pack(padx=20, pady=20)
        
        #
        lbl = tk.Label(open_frame, text="To get the metadata of an image, please open it here:")
        lbl.pack(expand=True)
        btn = tk.Button(
            open_frame,
            text="Open",
            command=lambda: (
                select_image(img_lbl, tree)
                # get_data(tree)
            )
        )
        btn.pack(padx=10, pady=10)        

        
        #        
        root.mainloop()
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import filedialog 
from scorpion import EXTS
from PIL import Image, ImageTk


def on_close(root):
    print("\nClosing Scorpion")
    root.destroy()


def check_exts(format: str, exts: list[str]) -> bool:
    return format.lower() in exts


def get_data(file: str, exts: list[str]) -> None:    
    try:
        with Image.open(file) as img:
            if img.format is None or not check_exts(img.format, exts):
                print(f"Format not recognized: {file}")
            else:
                print_attributes(img, file)
                print_exif(img)
    except OSError as e:
        print(f"Can't open {file}: {e}")


def get_photo(file: str, exts: list[str]) -> ImageTk.PhotoImage | None:
    try:
        with Image.open(file) as img:
            if img.format is None or not check_exts(img.format, exts):
                print(f"Format not recognized: {file}")
            else:                
                img.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(img)                    
                return photo                
    except OSError as e:
        print(f"Can't open {file}: {e}")


def select_image(img_lbl):
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

def main():
    try:
        print("Opening Scorpion\n")
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
        root.title("Scorpion")
        # root.geometry("1000x600")
        main_frame = tk.Frame(root, width=900, height=500)
        # main_frame.pack_propagate(False)
        main_frame.pack(padx=20, pady=20)

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        # main_frame.rowconfigure(0, weight=1)
        # main_frame.rowconfigure(1, weight=1)

        open_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
        open_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        preview_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
        preview_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        metadata_frame = tk.Frame(main_frame, borderwidth=1, relief="solid")
        metadata_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # 
        img_lbl = tk.Label(preview_frame, text="image preview")
        img_lbl.pack()
        data_lbl = tk.Label(metadata_frame, text="metadata")
        data_lbl.pack()

        #
        lbl = tk.Label(open_frame, text="To get the metadata of an image, please open it here:")
        lbl.pack(expand=True)
        btn = tk.Button(
            open_frame,
            text="Open",
            command=lambda: (
                select_image(img_lbl),
                get_data(data_lbl)
            )
        )
        btn.pack(padx=10, pady=10)        

        
        #        
        root.mainloop()
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

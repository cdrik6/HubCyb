import tkinter as tk
from tkinter import filedialog 
from scorpion import EXTS
from PIL import Image, ImageTk


def check_exts(format: str, exts: list[str]) -> bool:
    return format.lower() in exts


def get_data(files: list[str], exts: list[str]) -> None:
    for file in files:
        try:
            with Image.open(file) as img:
                if img.format is None or not check_exts(img.format, exts):
                    print(f"Format not recognized: {file}")
                else:
                    img = Image.open(file)
                    img.thumbnail((500, 400))
                    photo = ImageTk.PhotoImage(img)
                    image_label.config(image=photo)
                    image_label.image = photo
        except OSError as e:
            print(f"Can't open {file}: {e}")


def on_close(root):
    print("\nClosing Scorpion")
    root.destroy()


def select_image():
    filename = filedialog.askopenfilename(
        title = "Select an image",
        filetypes = [
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )
    if not filename:
        return
    get_data([filename], EXTS)

    
    
    
    
    


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

        lbl = tk.Label(open_frame, text="To get the metadata of an image, please open it here:")
        lbl.pack(expand=True)
        btn = tk.Button(open_frame, text="Open", command=select_image)    
        btn.pack(padx=10, pady=10)

        # lbl = tk.Label(root)
        # lbl.grid(row=1, column=0)
        lbl2 = tk.Label(preview_frame, text="test preview")
        lbl2.pack()
        lbl3 = tk.Label(metadata_frame, text="test meta")
        lbl3.pack()
        

        # 
        
        root.mainloop()
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

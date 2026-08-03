import tkinter as tk
from tkinter import filedialog
from scorpion import EXTS, get_data


def on_close(root):
    print("Closing Scorpion")
    root.destroy()


def select_image():
    filename = filedialog.askopenfilename(
        title = "Select an image",
        filetypes = [
            ("Images", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )
    if filename:
        get_data([filename], EXTS)


def main():
    try:
        print("Opening Scorpion")
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
        root.title("Scorpion")
        # 

        lbl = tk.Label(root, text="Open an image")
        lbl.grid(row=0, column=0)

        lbl = tk.Label(root)
        lbl.grid(row=1, column=0)

        btn = tk.Button(root, text="Open", command=select_image)    
        btn.grid(row=2, column=0)

        # 
        
        root.mainloop()
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user")


if __name__ == "__main__":
    main()

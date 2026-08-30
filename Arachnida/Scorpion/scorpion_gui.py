import tkinter as tk
from tkinter import ttk
from scorpion import EXTS
from delete_gui import delete_all, delete_one
from modify_gui import modify
from metadata_gui import select_image, on_selected


def on_close(root):
    print("\nClosing Scorpion")
    root.destroy()


def main():
    try:
        print("Opening Scorpion\n")
        root = tk.Tk()
        root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
        root.title("Scorpion")
        root.geometry("600x800")

        open_frame = tk.Frame(root, borderwidth=1, relief="solid")
        open_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        image_frame = tk.Frame(root, borderwidth=1, relief="solid")
        image_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        data_frame = tk.Frame(root, borderwidth=1, relief="solid")
        data_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        mod_frame = tk.Frame(root, borderwidth=1, relief="solid")
        mod_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        del_frame = tk.Frame(root, borderwidth=1, relief="solid")
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

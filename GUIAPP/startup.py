import BPE
import tkinter as tk
import os
import zipfile
import traceback
import pyperclip
from tkinter import messagebox
import sys
import shutil
from tkinter import filedialog
import packagemanager

root = tk.Tk()
root.geometry("256x256+300+200")
root.configure(bg="#232323")
root.title("Beemod Package Editor (STARTUP) V.2")

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

def browse_file():
    file_path = filedialog.askopenfilename()
    path_entry.delete(0, 'end')
    path_entry.insert(0, file_path)

def fixvtf():
    with open(os.path.join(path,"config.bpe"),"r") as config:
        itemsdict = packagemanager.readfile(config.read())
    packagemanager.patch_vtfs(itemsdict)

def submit_path():
    path2 = path_entry.get()
    try:
        shutil.rmtree(os.path.join(path,"packages"))    
        os.makedirs(os.path.join(path,"packages"))
        with zipfile.ZipFile(path2, 'r') as zip_ref:
            txtfile = zip_ref.open('info.txt', 'r')
            txtlist = txtfile.read().decode().split("\n")
        if "//" in txtlist[0]:
            with open(os.path.join(path,"config.bpe"),"w") as config:
                config.write(path2)
            root.destroy()
            if check_var.get() == 1:
                fixvtf()
            BPE.intui()
        else:
            result = messagebox.askyesno("Error", "Not a BeePKG package!\nWould you like to open this anyways?\nYou may encounter errors by doing this.")
            if result == True:
                with open(os.path.join(path,"config.bpe"),"w") as config:
                    config.write(path2)
                root.destroy()
                if check_var.get() == 1:
                    fixvtf()
                BPE.intui()
    except Exception as error:
        pyperclip.copy(traceback.format_exc())
        messagebox.showerror("Error", traceback.format_exc(), detail= "This has been copied to the clipboard.")

path_label = tk.Label(root, text="Enter path to file:", bg="#232323",fg="#878787")
path_label.pack()

path_entry = tk.Entry(root, bg="#474747",fg="#878787")
path_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787")
browse_button.place(x=128,y=40)

submit_button = tk.Button(root, text="Submit", command=submit_path, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787")
submit_button.place(x=78,y=40)

check_var = tk.IntVar()
check_button = tk.Checkbutton(root, text="Patch VTFs", variable=check_var, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787")
check_button.place(x=86,y=65)

root.mainloop()
import BPE
import tkinter as tk
import os
import requests
from webbrowser import open as webopen
import zipfile
import traceback
import pyperclip
from tkinter import messagebox
import sys
import shutil
from tkinter import filedialog
import packagemanager

version = "2.0"

if "_DEV" not in version.upper():
    if requests.get("https://versioncontrol.orange-gamergam.repl.co/api/bpe").json() <= float(version):
        print("No updates are currently available.")
    else:
        versionask = messagebox.askyesno('Update',f'There is an update available. You are using ({version}) Newest is ({requests.get("https://versioncontrol.orange-gamergam.repl.co/api/bpe").json()})\nWould you like to download it?')
        if versionask == True:
            webopen("https://github.com/Areng14/BeePackageEditor/releases")
        else:
            pass

root = tk.Tk()
root.geometry("256x256+300+200")
root.config(bg="#232323")
root.resizable(False, False)
root.configure(bg="#232323")
root.title("Beemod Package Editor (STARTUP) V.2")

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

while os.path.isdir(os.path.join(path,"packages")):
    shutil.rmtree(os.path.join(path,"packages"), ignore_errors=True)


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
        while os.path.isdir(os.path.join(path,"packages")):
            shutil.rmtree(os.path.join(path,"packages"), ignore_errors=True)
        os.makedirs(os.path.join(path,"packages"))
        with zipfile.ZipFile(path2, 'r') as zip_ref:
            txtfile = zip_ref.open('info.txt', 'r')
            txtlist = txtfile.read().decode().split("\n")
        if "//" in txtlist[0]:
            with open(os.path.join(path,"config.bpe"),"w") as config:
                config.write(path2)
            root.destroy()
            if check_var.get() == 1:
                try:
                    fixvtf()
                except FileNotFoundError:
                    value = messagebox.askyesno("Error","During the patch vtf, we could not patch one of your vtfs. Would you like to load your package before it was patched?")
                    if value:
                        while os.path.isdir(os.path.join(path,"packages")):
                            shutil.rmtree(os.path.join(path,"packages"), ignore_errors=True)
                        os.makedirs(os.path.join(path,"packages"))
                        with zipfile.ZipFile(path2, 'r') as zip_ref:
                            txtfile = zip_ref.open('info.txt', 'r')
                            txtlist = txtfile.read().decode().split("\n")
            BPE.intui()
        else:
            result = messagebox.askyesno("Warning", "Not a BeePKG package!\nWould you like to open this anyways?\nYou may encounter errors by doing this.")
            if result == True:
                with open(os.path.join(path,"config.bpe"),"w") as config:
                    config.write(path2)
                root.destroy()
                if check_var.get() == 1:
                    try:
                        fixvtf()
                    except:
                        value = messagebox.askyesno("Error","During the patch vtf, we could not patch one of your vtfs. Would you like to load your package before it was patched?")
                        if value:
                            while os.path.isdir(os.path.join(path,"packages")):
                                shutil.rmtree(os.path.join(path,"packages"), ignore_errors=True)
                            os.makedirs(os.path.join(path,"packages"))
                            with zipfile.ZipFile(path2, 'r') as zip_ref:
                                txtfile = zip_ref.open('info.txt', 'r')
                                txtlist = txtfile.read().decode().split("\n")

                BPE.intui()
    except FileNotFoundError:
        froot = tk.Tk()
        froot.withdraw()
        messagebox.showerror(title="Error", message=f'Could not read editoritems.txt from one of your items!\nPlease check your info.txt')
        froot.destroy()
        sys.exit()
    except Exception as error:
        pyperclip.copy(traceback.format_exc())
        messagebox.showerror("Error", traceback.format_exc(), detail= "This has been copied to the clipboard.")

def loadlast():
    try:
        with open(os.path.join(path,"config.bpe"),"r") as file:
            choice = messagebox.askyesno("Info",f'Do you want to load "{os.path.basename(file.read())}"?')
        if choice == True:
            root.destroy()
            BPE.intui()
    except FileNotFoundError:
        messagebox.showerror("Error", "We could not find your most recent file.")
    except Exception as error:
        pyperclip.copy(traceback.format_exc())
        messagebox.showerror("Error", traceback.format_exc(), detail= "This has been copied to the clipboard.")

def opendis():
    webopen("https://discord.gg/gdKhV2jGyh")

def opengit():
    webopen("https://github.com/Areng14/BeePackageEditor")

root.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

path_label = tk.Label(root, text="Enter path to file:", bg="#232323",fg="#878787")
path_label.pack()

path_entry = tk.Entry(root, bg="#474747",fg="#878787")
path_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787")
browse_button.place(x=128,y=40)

submit_button = tk.Button(root, text="Submit", command=submit_path, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787")
submit_button.place(x=78,y=40)

submit_button = tk.Button(root, text="    Load Recent    ", command=loadlast, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787")
submit_button.place(x=78,y=65)

check_var = tk.IntVar()
check_button = tk.Checkbutton(root, text="Patch VTFs", variable=check_var, bg="#232323",fg="#878787",activeforeground="#878787",activebackground="#232323")
check_button.place(x=86,y=90)

desc_button = tk.Button(root, text="Discord Server", command=opendis, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787",width=13)
desc_button.place(x=80,y=160)

desc_button = tk.Button(root, text="Github", command=opengit, bg="#232323",fg="#878787",activeforeground="#232323",activebackground="#878787",width=13)
desc_button.place(x=80,y=192)


root.mainloop()
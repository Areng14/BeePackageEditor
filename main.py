import os
import tkinter as tk
from tkinter import *
import pyperclip
import traceback
from tkinter import filedialog,messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage, Tk, Button
from PIL import Image, ImageTk
from functools import partial
import re
import log
import time
import json
import shutil
import sys
import assetmanager
import packagemanager

ver = 3.0

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
    log.loginfo(f"Local Path is __file__")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")
    log.loginfo(f"Local Path is sys.executable")

assetmanager.loadconfig()

themes = {
    "dark" : [
        "#878787",
        "#232323",
        "#4d4d4d",
        "#878787"
    ],
    "light" : [
        "#474747",
        "#dedede",
        "#7a7a7a",
        "#FFFFFF"
    ]
}

ctheme = "dark"

config = assetmanager.config

if not config["package"] or not os.path.isfile(config["package"]):
    pakdir = filedialog.askopenfilename(filetypes=[('Bee Package', '*.bee_pack'), ('ZIPs', '*.zip')])
    assetmanager.writeconfig("package",pakdir)
trn = time.time()
log.loginfo(f'Reading {config["package"]}')

def forcedelete(dir):
    while os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=True)
forcedelete(packagemanager.packagesdir)

items = packagemanager.readfile(config["package"],extract=True)
log.loginfo(f'Finished Reading {config["package"]} ({round(time.time() - trn,2)}s)')

if not os.path.isdir(os.path.join(path,"modules")):
    os.makedirs(os.path.join(path,"modules"))

log.loginfo(f'Starting UI')
trn = time.time()
itemmenu = tk.Tk()
itemmenu.title(f"Item Select")
itemmenu.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

status_bar = tk.Label(itemmenu, text="No item selected", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

log.loginfo(f'Creating grid')

sorted_items = None
selid = None
buttons = []

def on_click(row, col, frame, shift=False):
    global selected_frame, selid, buttons

    if not shift:
        if selected_frame:
            selected_frame.config(bg='white')

    frame.config(bg=("#3ba7ff"))
    selected_frame = frame

    # Correctly calculate the index of the selected item
    index = row * 16 + col
    if index < len(sorted_items):
        selid = sorted_items[index]
        log.loginfo(f"Clicked on {selid[0]}")
    else:
        pass

    for button in buttons:
        button.config(state=tk.NORMAL)
    module.deiconify()
    status_bar.config(text=f"Selected Item: {selid[1]}")


selected_frame = None

def updateitem():
    global items
    items = packagemanager.readfile(config["package"],extract=False)


def refreshitems():
    global sorted_items, selected_frame, items

    for widget in itemmenu.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    button_frame = Frame(itemmenu)
    button_frame.pack(fill='both', expand=True)

    integer_keys = filter(lambda k: isinstance(k, int), items.keys())
    sorted_items = [items[k] for k in sorted(integer_keys)]
    selected_frame = None
    itemmenu.geometry(f"1088x{74 * (round(len(items) / 16) + 1)}+300+200")

    for row in range(round(len(items) / 16) + 1):
        for col in range(16):
            index = row * 16 + col
            if index < len(sorted_items):
                item_data = sorted_items[index]
                properties_file_path = os.path.join(packagemanager.packagesdir, "items", item_data[2], "properties.txt")
                
                try:
                    with open(properties_file_path) as file:
                        image_path = re.findall(r'"0"\s+"([^"]+)"', file.read())[0]
                        image_path = os.path.join(packagemanager.packagesdir, "resources", "BEE2", "items", image_path)

                        pil_image = Image.open(image_path)
                except (IndexError, FileNotFoundError):
                    image_path = os.path.join(path, "imgs", "error.png")
                    pil_image = Image.open(image_path)

                resized_image = pil_image.resize((64, 64), Image.Resampling.LANCZOS)
                if item_data[3] == True:
                    white_image = Image.new('RGB', resized_image.size, color='white')
                    try:
                        resized_image = Image.blend(resized_image, white_image, alpha=0.75)
                    except ValueError:
                        pass
                image = ImageTk.PhotoImage(resized_image)

                frame = Frame(button_frame, bg='white', borderwidth=2)
                frame.grid(row=row, column=col)
                button = Button(frame, image=image, command=partial(on_click, row, col, frame), borderwidth=0, highlightthickness=0)
                button.image = image
                button.pack()
            else:
                continue

# Add an event listener to handle shift-clicks
itemmenu.bind("<Shift-Button-1>", lambda event: on_click(event.widget.row, event.widget.col, event.widget, shift=True))

refreshitems()

log.loginfo(f'Loading modules')
trn = time.time()

module = tk.Toplevel()
module.title("Item Commands")
module.geometry("600x400")
module.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))
module.withdraw()
module.protocol("WM_DELETE_WINDOW", module.withdraw)
status_bar_frame = tk.Frame(module)
status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)
status_bar2 = tk.Label(status_bar_frame, text="", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar2.pack(fill=tk.X)

def on_hover(event, button_name):
    status_bar2.config(text=f"{button_name.title()}")

def on_leave(event):
    status_bar2.config(text="")

def run_script(script_path):
    restricted_globals = {
        "item" : selid,
        'themes' : themes,
        'ctheme' : ctheme,
        'updateitem' : updateitem,
        'refreshitems' : refreshitems,
        'log' : log,
        'packagemanager' : packagemanager,
        'assetmanager' : assetmanager,
        'messagebox' : messagebox
    }

    try:
        with open(script_path, "r") as file:
            code = compile(file.read(), script_path, 'exec')
            exec(code, restricted_globals)
    except Exception as error:
        error_message = str(error)
        error_traceback = traceback.format_exc()
        pyperclip.copy(error_message)
        log.logerror(error_traceback)
        messagebox.showerror("Error", error_message, detail="This has been copied to the clipboard.")
        # Handle the exception as needed


row = 0
col = 0

button_frame = tk.Frame(module)
button_frame.pack(fill='both', expand=True)

for plugin in os.listdir(os.path.join(path, "modules")):
    with open(os.path.join(path, "modules", plugin, "info.txt"), "r") as info:
        try:
            plugininfo = json.load(info)
        except json.JSONDecodeError:
            messagebox.showerror("Error",f"Invalid Syntax!\n{plugin}")

        for key in list(plugininfo.keys())[1:]:
            script_info = plugininfo[key]

            icon_path = os.path.join(path, "modules", plugin, script_info["icon"])
            if not os.path.isfile(icon_path):
                icon_path = os.path.join(path,"imgs","error.png")
            pil_image = Image.open(icon_path)
            pil_image = pil_image.resize((64, 64))
            icon = ImageTk.PhotoImage(pil_image)

            btn = tk.Button(module, image=icon, state=tk.DISABLED, command=lambda s=script_info["script"]: run_script(os.path.join(path, "modules", plugin, s)))
            btn.image = icon
            buttons.append(btn)
            btn.grid(in_=button_frame, row=row, column=col)

            btn.bind("<Enter>", lambda event, info=f"{plugin} - {key}": on_hover(event, info))
            btn.bind("<Leave>", on_leave)

            col += 1
            if col > 3: 
                col = 0
                row += 1

log.loginfo(f'Loaded modules ({round(time.time() - trn,2)}s)')

log.loginfo(f'Started UI ({round(time.time() - trn,2)}s)')
itemmenu.mainloop()

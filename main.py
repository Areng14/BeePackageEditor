import os
import tkinter as tk
from tkinter import *
import pyperclip
import requests
from webbrowser import open as open_url
from math import ceil
import traceback
import keyboard
from tkinter import filedialog,messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage, ttk, Button
from PIL import Image, ImageTk
from functools import partial
import srctools
import vpk
import winreg
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
    pakdir = filedialog.askopenfilename(filetypes=[('Bee Package', '*.bee_pack;*.zip')])
    config["package"] = pakdir
    assetmanager.updateconfig(config)
trn = time.time()
log.loginfo(f'Reading {config["package"]}')

def forcedelete(dir):
    while os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=True)

forcedelete(packagemanager.packagesdir)

try:
    items = packagemanager.readfile(config["package"],extract=True)
except Exception as error:
    error_traceback = traceback.format_exc()
    pyperclip.copy(error_traceback)
    log.logerror(error_traceback)
    messagebox.showerror("Error", error_traceback, detail="This has been copied to the clipboard.\n\nYour config file has been cleared to prevent startup issues.")
    config = {
        "package": "",
        "plugins": {},
        "theme": 0
    }
    with open(os.path.join(os.path.join(os.environ.get('APPDATA'), "BPE_v3"), "BPE.config"), "w") as f_write:
        json.dump(config, f_write)
    sys.exit(0)
log.loginfo(f'Finished Reading {config["package"]} ({round(time.time() - trn,2)}s)')

if not os.path.isdir(os.path.join(path,"modules")):
    os.makedirs(os.path.join(path,"modules"))

log.loginfo(f'Starting UI')
trn = time.time()
itemmenu = tk.Tk()
itemmenu.title(f"Item Select")
itemmenu.resizable(False,False)
itemmenu.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

def openpkg():
    global items
    pakdir = filedialog.askopenfilename(filetypes=[('Bee Package', '*.bee_pack;*.zip')])
    config["package"] = pakdir
    assetmanager.updateconfig(config)
    trn = time.time()
    forcedelete(packagemanager.packagesdir)
    log.loginfo(f'Reading {config["package"]}')
    try:
        items = packagemanager.readfile(config["package"],extract=True)
    except Exception as error:
        error_traceback = traceback.format_exc()
        pyperclip.copy(error_traceback)
        log.logerror(error_traceback)
        messagebox.showerror("Error", error_traceback, detail="This has been copied to the clipboard.")
    updateitem()
    refreshitems()
    log.loginfo(f'Finished Reading {config["package"]} ({round(time.time() - trn,2)}s)')
    status_bar = ttk.Label(itemmenu, text="No item selected", relief=tk.SUNKEN, anchor=tk.W)

def reloadpkg():
    global items
    items = packagemanager.readfile(config["package"],extract=True)
    updateitem()
    refreshitems()
    log.loginfo("Reload Finished")

def savepkg():
    filepath = config["package"]
    basename = os.path.splitext(os.path.basename(filepath))[0]
                                                    

    # Create a zip archive
    shutil.make_archive(basename, "zip", packagemanager.packagesdir)

    os.remove(config["package"])
    shutil.move(os.path.join(path,f"{basename}.zip"),config["package"])
    messagebox.showinfo("Info","Saved package!")

    # Log information
    log.loginfo("Saved!")

def saveaspkg():
    filepath = config["package"]
    basename = os.path.splitext(os.path.basename(filepath))[0]

    filetypes = (("Beemod Package", "*.bee_pack"), ("All Files", "*.*"))

    # Ask user to specify the save location
    file_save_path = filedialog.asksaveasfilename(filetypes=filetypes, initialfile=basename)
    print(file_save_path)

    if not file_save_path:
        messagebox.showwarning("Warning", "Save operation cancelled.")
        return  # Exit the function if no file was selected

    # Create a zip archive
    shutil.make_archive(basename, "zip", packagemanager.packagesdir)

    # Move and rename the file with the correct extension
    try:
        zip_file_path = os.path.join(path, f"{basename}.zip")
        shutil.move(zip_file_path, f"{file_save_path}.bee_pack")
    except Exception as e:
        messagebox.showerror("Error", f"Error in saving file: {e}")
        return

    config["package"] = f"{file_save_path}.bee_pack"
    assetmanager.updateconfig(config)

    messagebox.showinfo("Info", f"Saved package as {os.path.basename(file_save_path)}!")
    log.loginfo(f"Saved as {os.path.basename(file_save_path)}")

def clearcfg():
    appdata_path = os.path.join(os.environ.get('APPDATA'), "BPE_v3")
    config_path = os.path.join(appdata_path, "BPE.config")
    config = {
        "package": "",
        "plugins": {},
        "theme": 0
    }
    with open(config_path, "w") as f_write:
        json.dump(config, f_write)
    messagebox.showwarning("Warning","Cleared configuration file")
    sys.exit(1)

status_bar = ttk.Label(itemmenu, text="No item selected", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

log.loginfo(f'Creating grid')

sorted_items = None
selected_frames = {}
selid = []
buttons = []
last_click_time = 0

def change_frame_color(button):
    parent_name = button.winfo_parent()
    parent_frame = button._nametowidget(parent_name)
    parent_frame.config(bg="#3ba7ff")  # Change frame color to blue

def on_click(row, col, frame, ctrl=False):
    global selected_frame, selid, buttons, selected_frames, last_click_time

    current_click_time = time.time()
    if current_click_time - last_click_time < 0.3:
        return 

    last_click_time = current_click_time

    index = row * 16 + col
    if index < len(sorted_items):
        item_info = sorted_items[index]

        if ctrl:
            if item_info in selid:
                selid.remove(item_info)
                if frame.winfo_exists():
                    frame.config(bg='white')
                del selected_frames[item_info[0]]
            else:
                if item_info not in selid:
                    selid.append(item_info)
                    if frame.winfo_exists():
                        frame.config(bg="#3ba7ff")
                    selected_frames[item_info[0]] = frame
        else:
            for id, frm in selected_frames.items():
                if frm.winfo_exists():
                    frm.config(bg='white')
            selected_frames = {item_info[0]: frame}
            selid = [item_info]
            if frame.winfo_exists():
                frame.config(bg="#3ba7ff")

        selected_frame = frame
        log.loginfo(f"Selected: {selid}")
    else:
        pass

    for button in buttons:
        button.config(state=tk.NORMAL)
    module.deiconify()
    status_bar.config(text=f"Selected Items: {', '.join([str(item[1]) for item in selid])}")

selected_frame = None

def updateitem():
    global items
    items = packagemanager.readfile(config["package"],extract=False)

first_item_frame = None

firsttime = 0

def refreshitems():
    global sorted_items, selected_frame, items, first_item_frame, firsttime
    try:

        # Destroy all frames before creating new ones
        for widget in itemmenu.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()

        # Create a new frame to hold the buttons
        button_frame = Frame(itemmenu)
        button_frame.pack(fill='both', expand=True)

        # Sort and prepare the items
        integer_keys = filter(lambda k: isinstance(k, int), items.keys())
        sorted_items = [items[k] for k in sorted(integer_keys)]
        selected_frame = None  # Reset selected frame
        itemmenu.geometry(f"{1152}x{74 * (ceil(len(items) / 16) + 1)}")

        # Create buttons for each item
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
                    if item_data[3]:
                        white_image = Image.new(resized_image.mode, resized_image.size, (255, 255, 255))
                        if resized_image.mode != 'RGB':
                            white_image = white_image.convert(resized_image.mode)
                        try:
                            resized_image = Image.blend(resized_image, white_image, alpha=0.8)
                        except ValueError as e:
                            pass
                    image = ImageTk.PhotoImage(resized_image)

                    # Create frame for each button
                    frame = Frame(button_frame, bg='white', borderwidth=2)
                    if row == 0 and col == 0:
                        first_item_frame = frame
                    frame.grid(row=row, column=col)

                    # Ensure the button doesn't cover the entire frame
                    button = Button(frame, image=image, command=partial(on_click, row, col, frame), borderwidth=0, highlightthickness=0)
                    button.image = image  # Keep a reference to avoid garbage collection
                    button.row = row
                    button.col = col
                    button.pack(padx=2, pady=2)  # Add some padding to allow frame background to be visible

                else:
                    continue
    except Exception as error:
        error_traceback = traceback.format_exc()
        pyperclip.copy(error_traceback)
        log.logerror(error_traceback)
        messagebox.showerror("Error", error_traceback, detail="This has been copied to the clipboard.")
    if firsttime == 1:
        on_click(0, 0, first_item_frame, ctrl=False)

refreshitems()

def on_ctrl_click(event):
    widget = event.widget
    on_click(widget.row, widget.col, widget, ctrl=True)

itemmenu.bind("<Control-Button-1>", on_ctrl_click)

#Shortcut
log.loginfo(f'Loading shortcut')
trn = time.time()

shortcuts = {
    'ctrl+r': reloadpkg,
    'ctrl+s': savepkg,
}

def bind_shortcut():
    for key_combination, function in shortcuts.items():
        keyboard.add_hotkey(key_combination, function)

bind_shortcut()
log.loginfo(f'Loaded shortcuts ({round(time.time() - trn,2)}s)')

log.loginfo(f'Loading modules')
trn = time.time()

module = tk.Toplevel()
module.title("Item Commands")
module.geometry(f"600x400")
module.resizable(False,False)
module.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))
module.withdraw()
module.protocol("WM_DELETE_WINDOW", module.withdraw)
status_bar_frame = ttk.Frame(module)
status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X)
status_bar2 = ttk.Label(status_bar_frame, text="", relief=tk.SUNKEN, anchor=tk.W)
status_bar2.pack(fill=tk.X)

def on_hover(event, button_name):
    status_bar2.config(text=f"{button_name.title()}")

def on_leave(event):
    status_bar2.config(text="")

def retreive_pdata(plugin_name,key):
    try:
        log.loginfo(f"{plugin_name} requesting {key} from data. contents: {config['plugins'][plugin_name][key]}")
        return config["plugins"][plugin_name][key]
    except:
        log.loginfo(f"{plugin_name} requesting nonexistant key from data.")
        return None

def save_pdata(plugin_name,key,data):
    log.loginfo(f"{plugin_name} writing data to {key}. contents: {data}")
    config["plugins"][plugin_name][key] = data
    assetmanager.updateconfig(config)

def openurl(plugin_name,url):
    log.logwarn(f"{plugin_name} is trying to open {url}")
    open_url(url)
    return True

def run_script(script_path,plugin_name):
    global buttons
    print("hi")
    #Disable all buttons to prevent spam
    if selid:
        for button in buttons:
            button.config(state=tk.DISABLED)
        for index, sselid in enumerate(selid):
            restricted_globals = {
                "mselect" : True if len(selid) > 1 else False,
                "mselection" : selid,
                "itemcount" : index,
                'updateitem' : updateitem,
                'refreshitems' : refreshitems,
                "item" : sselid,
                "plugin_name" : plugin_name,
                "get_plugin_data" : retreive_pdata,
                "save_plugin_data" : save_pdata,
                'themes' : themes,
                'ctheme' : ctheme,
                'log' : log,
                're' : re,
                'srctools' : srctools,
                'vpk' : vpk,
                'shutil' : shutil,
                'os' : os,
                'winreg' : winreg,
                'packagemanager' : packagemanager,
                'filedialog' : filedialog,
                'requests' : requests,
                'assetmanager' : assetmanager,
                'messagebox' : messagebox
            }

            try:
                with open(script_path, "r") as file:
                    code = compile(file.read(), script_path, 'exec')
                    exec(code, restricted_globals)
            except Exception as error:
                error_traceback = traceback.format_exc()
                pyperclip.copy(error_traceback)
                log.logerror(error_traceback)
                messagebox.showerror("Error", error_traceback, detail="This has been copied to the clipboard.")
            for button in buttons:
                button.config(state=tk.NORMAL)
    else:
        messagebox.showerror("Error", "Please select an item first!")

menubar = None

def showmodule():
    module.deiconify()

def genfilemenu():
    global menubar
    #File menu
    menubar = tk.Menu(itemmenu)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=openpkg)
    filemenu.add_command(label="Save", command=savepkg)
    filemenu.add_command(label="Save As", command=saveaspkg)
    filemenu.add_separator()
    filemenu.add_command(label="Clear config file", command=clearcfg)
    filemenu.add_command(label="Reload File", command=reloadpkg)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=itemmenu.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    viewmenu = tk.Menu(menubar, tearoff=0)
    viewmenu.add_command(label="Show Item Menu", command=showmodule)
    menubar.add_cascade(label="View", menu=viewmenu)

    itemmenu.config(menu=menubar)

buttons2 = []

def loadplugin():
    global menubar
    
    row = 0
    col = 0
    for i in range(menubar.index(tk.END), 0, -1):
        menubar.delete(i)

    genfilemenu()

    button_frame = ttk.Frame(module)
    button_frame.pack(fill='both', expand=True)

    menu_structure = {}

    def add_to_menu_structure(structure, tab, group, item_name, script_info):
        """
        Add an entry to the menu structure.
        """
        if tab not in structure:
            structure[tab] = {}

        if group not in structure[tab]:
            structure[tab][group] = []

        structure[tab][group].append((item_name, script_info))

    for plugin in os.listdir(os.path.join(path, "modules")):
        file_path = os.path.join(path, "modules", plugin, "info.txt")
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()

            json_str = "".join([line for line in lines if not line.strip().startswith('#')])

            plugininfo = json.loads(json_str)
        except json.JSONDecodeError:
            messagebox.showerror("Error", f"Invalid Syntax!\n{plugin}")

        module.geometry(f"600x{ceil((len(plugininfo.keys()) + 1) * 16)}")

        for key in list(plugininfo.keys())[1:]:
            script_info = plugininfo[key]
            # Check if the type is 'item'
            if script_info.get("type").lower() == "item":
                # Existing logic for types other than 'item'
                icon_path = os.path.join(path, "modules", plugin, script_info["icon"])
                if not os.path.isfile(icon_path):
                    icon_path = os.path.join(path, "imgs", "error.png")
                pil_image = Image.open(icon_path)
                pil_image = pil_image.resize((64, 64))
                icon = ImageTk.PhotoImage(pil_image)
                if plugin not in config["plugins"]:
                    config["plugins"][plugin] = {}
                btn = Button(module, image=icon, command=lambda s=script_info["script"]: run_script(os.path.join(path, "modules", plugin, s),plugin), borderwidth=0, highlightthickness=0)
                btn.image = icon
                buttons2.append(btn)
                btn.grid(in_=button_frame, row=row, column=col)
                btn.bind("<Enter>", lambda event, info=f"{plugin} - {key}": on_hover(event, info))
                btn.bind("<Leave>", on_leave)
                col += 1
                if col > 3:
                    col = 0
                    row += 1
            elif script_info.get("type").lower() == "menu":
                # Add menu info to the structure
                tab = script_info.get("tab")
                group = script_info.get("group")
                add_to_menu_structure(menu_structure, tab, group, key, script_info)

    for tab_name, groups in menu_structure.items():
        tab_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=tab_name, menu=tab_menu)
        
        for group_index, (group_name, items) in enumerate(groups.items()):
            # Adding a separator before each group except the first
            if group_index > 0:
                tab_menu.add_separator()
            for item_name, item_info in items:
                if "script" in item_info:
                    script_path = item_info["script"]
                    command = lambda script=script_path, plugin_name=plugin: run_script(os.path.join(path, "modules", plugin_name, script), plugin_name)
                    # Initially disabling the menu items
                    tab_menu.add_command(label=item_name, command=command)
                if "link" in item_info:
                    link = item_info["link"]
                    command = lambda link2=link, plugin_name=plugin: openurl(plugin_name,link2)
                    # Initially disabling the menu items
                    tab_menu.add_command(label=item_name, command=command)

assetmanager.updateconfig(config)
genfilemenu()
loadplugin()
log.loginfo(f'Loaded modules ({round(time.time() - trn,2)}s)')

log.loginfo(f'Started UI ({round(time.time() - trn,2)}s)')
on_click(0, 0, first_item_frame, ctrl=False)
firsttime = 1
itemmenu.mainloop()


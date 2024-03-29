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
from pypresence import Presence
import threading
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

def reset_idle_timer(event=None):
    global last_interaction_time
    last_interaction_time = time.time()

def check_idle_state():
    global last_interaction_time, is_idle
    current_time = time.time()
    if current_time - last_interaction_time > idle_threshold:
        if not is_idle:
            is_idle = True
    else:
        if is_idle:
            is_idle = False
    itemmenu.after(1000, check_idle_state)  # Check every second

def discord_rich_presence():
    global config, is_idle
    with open(os.path.join(path, "discordRP.txt"), "r") as file:
        client_id = file.read().strip()

    RPC = Presence(client_id)
    RPC.connect()

    version_text = f"Beemod Package Editor {ver}"

    RPC.update(
        details="Editing a package",
        state=f'Editing {os.path.splitext(os.path.basename(config["package"]))[0]} ({"Idling" if is_idle else "Active"})',
        large_image="default",
        large_text=version_text
    )

    while True:
        RPC.update(
            details="Editing a package", 
            state=f'Editing {os.path.splitext(os.path.basename(config["package"]))[0]} ({"Idling" if is_idle else "Active"})',
            large_image="default",
            large_text=version_text
        )
        time.sleep(15)

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
threading.Thread(target=discord_rich_presence, daemon=True).start()
trn = time.time()
itemmenu = tk.Tk()
itemmenu.title(f"Item Select")
itemmenu.resizable(False,False)
itemmenu.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

last_interaction_time = time.time()
idle_threshold = 60
is_idle = False

itemmenu.bind("<Any-KeyPress>", reset_idle_timer)
itemmenu.bind("<Any-Motion>", reset_idle_timer)

itemmenu.after(1000, check_idle_state)

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
    loadsign()
    loadstyle()
    log.loginfo(f'Finished Reading {config["package"]} ({round(time.time() - trn,2)}s)')
    status_bar = ttk.Label(itemmenu, text="No item selected", relief=tk.SUNKEN, anchor=tk.W)

def reloadpkg():
    global items
    items = packagemanager.readfile(config["package"],extract=True)
    updateitem()
    refreshitems()
    loadsign()
    loadstyle()
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

def on_click(row, col, iframe, ctrl=False):
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
                if iframe.winfo_exists():
                    iframe.config(bg='white')
                del selected_frames[item_info[0]]
            else:
                if item_info not in selid:
                    selid.append(item_info)
                    if iframe.winfo_exists():
                        iframe.config(bg="#3ba7ff")
                    selected_frames[item_info[0]] = iframe
        else:
            for id, frm in selected_frames.items():
                if frm.winfo_exists():
                    frm.config(bg='white')
            selected_frames = {item_info[0]: iframe}
            selid = [item_info]
            if iframe.winfo_exists():
                iframe.config(bg="#3ba7ff")

        selected_frame = iframe
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
    if not items:
        return
    
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
                    iframe = Frame(button_frame, bg='white', borderwidth=2)
                    if row == 0 and col == 0:
                        first_item_frame = iframe
                    iframe.grid(row=row, column=col)

                    # Ensure the button doesn't cover the entire frame
                    button = Button(iframe, image=image, command=partial(on_click, row, col, iframe), borderwidth=0, highlightthickness=0)
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
                'loadsign' : loadsign,
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
                'messagebox' : messagebox,
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

def showsign():
    signage.deiconify()

def newitem():
    pass

def newsign():
    image_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not image_file:
        return

    try:
        os.makedirs(os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage"))
    except FileExistsError:
        pass
    shutil.copy(image_file,os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage",os.path.basename(image_file)))

    pil_image = Image.open(os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage", os.path.basename(image_file)))
    resized_image = pil_image.resize((64, 64), Image.Resampling.LANCZOS)
    if has_transparency(resized_image):
        signage_frame = messagebox.askyesno("Signage","Would you like to add the signage background to your image?")
        if signage_frame:
            background = Image.open(os.path.join(path,"imgs","signage_blank.png"))
            resized_image = pil_image.resize((48, 48), Image.Resampling.LANCZOS)
            if background.mode != 'RGBA':
                background = background.convert('RGBA')
            if resized_image.mode != 'RGBA':
                resized_image = resized_image.convert('RGBA')

            alpha_mask = resized_image.split()[3]

            x = (background.width - resized_image.width) // 2
            y = (background.height - resized_image.height) // 2

            background.paste(resized_image, (x, y), alpha_mask)
            resized_image = background
    rgba_image_path = os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage", os.path.basename(image_file))
    resized_image.save(rgba_image_path)

    name = os.path.splitext(os.path.basename(image_file))[0].replace("_"," ").title()
    id = os.path.splitext(os.path.basename(image_file))[0].replace(" ","_").upper()

    newdata = [id,name,None,f"signage/{os.path.basename(image_file)}",f'signage/{f"{os.path.splitext(os.path.basename(image_file))[0]}.vtf"}']

    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "r") as file:
        file_content = file.read()

    updated_content = file_content + f"\n{get_signage_block(newdata)}"

    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "w") as file:
        file.write(updated_content)

    assetmanager.format_file(os.path.join(packagemanager.packagesdir, "info.txt"))

    loadsign()

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

    editmenu = tk.Menu(menubar, tearoff=0)
    new_menu = tk.Menu(editmenu, tearoff=0)
    editmenu.add_cascade(label="New", menu=new_menu)
    
    new_menu.add_command(label="New Item", command=newitem)
    new_menu.add_command(label="New Signage", command=newsign)

    menubar.add_cascade(label="Edit", menu=editmenu)

    viewmenu = tk.Menu(menubar, tearoff=0)
    viewmenu.add_command(label="Show Item Menu", command=showmodule)
    viewmenu.add_command(label="Show Signage Menu", command=showsign)
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

#Signage Adder
signage = tk.Toplevel()
signage.title("Signages")
signage.geometry(f"304x500")
signage.resizable(False,False)
signage.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))
signage.protocol("WM_DELETE_WINDOW", signage.withdraw)
status_bar_frame3 = ttk.Frame(signage)
status_bar_frame3.pack(side=tk.BOTTOM, fill=tk.X)
status_bar3 = ttk.Label(status_bar_frame3, text="", relief=tk.SUNKEN, anchor=tk.W)
status_bar3.pack(fill=tk.X)

signagedict = {}
signagebutton = []

def findsignkey(id):
    itemcall = id
    for x in signagedict:
        if itemcall in signagedict[x][0]:
            return x

def get_signage_block(signage_id):
    if signage_id[2]:
        return (
            '"Signage"\n'
            '\t{\n'
            f'\t"ID" "{signage_id[0]}"\n'
            f'\t"Name" "{signage_id[1]}"\n'
            f'\t"Secondary" "{signage_id[2]}"\n'
            '\t"Styles"\n'
            '\t\t{\n'
            '\t\t"BEE2_CLEAN"\n'
            '\t\t\t{\n'
            f'\t\t\t"icon"    "{signage_id[3]}"\n'
            f'\t\t\t"overlay" "{signage_id[4]}"\n'
            '\t\t\t}\n'
            '\t\t}\n'
            '\t}\n'
        )
    else:
        return (
            '"Signage"\n'
            '\t{\n'
            f'\t"ID" "{signage_id[0]}"\n'
            f'\t"Name" "{signage_id[1]}"\n'
            '\t"Styles"\n'
            '\t\t{\n'
            '\t\t"BEE2_CLEAN"\n'
            '\t\t\t{\n'
            f'\t\t\t"icon"    "{signage_id[3]}"\n'
            f'\t\t\t"overlay" "{signage_id[4]}"\n'
            '\t\t\t}\n'
            '\t\t}\n'
            '\t}\n'
        )

def makevtf(pathtopng):
    VTFTarget = Image.open(pathtopng)
    width, height = VTFTarget.size
    vtf = srctools.VTF(width, height)
    vtf.get().copy_from(VTFTarget.tobytes())
    vtf_path = os.path.join(path,pathtopng.replace(os.path.basename(pathtopng), ""),os.path.splitext(os.path.basename(pathtopng))[0]+".vtf")
    with open(vtf_path, "wb") as f:
        vtf.save(f)

def delete_sign(event, signage_data):
    if not messagebox.askyesno("Warning",f"You are about to remove {signage_data[1]} peramently.\nAre you sure you want to do this?"):
        return

    os.remove(os.path.join(packagemanager.packagesdir, "resources", "BEE2", f"{signage_data[3]}"))
    os.remove(os.path.join(packagemanager.packagesdir, "resources", "materials", "signage", f"{os.path.basename(signage_data[4])}.vtf"))

    try:
        os.remove(os.path.join(packagemanager.packagesdir, "resources", "materials", "signage", f"{os.path.basename(signage_data[4])}.vmt"))
    except FileNotFoundError:
        pass

    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "r") as file:
        file_content = file.read()

    updated_content = file_content.replace(get_signage_block(signage_data), "")

    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "w") as file:
        file.write(updated_content)

    assetmanager.format_file(os.path.join(packagemanager.packagesdir, "info.txt"))

    loadsign()

def has_transparency(image):
    try:
        return image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info)
    except IOError:
        return False

def chooseimage(signage_data):
    image_file = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not image_file:
        return

    #Start
    #Copy image to bee2/signage folder
    try:
        os.makedirs(os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage"))
    except FileExistsError:
        pass
    shutil.copy(image_file,os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage",os.path.basename(image_file)))

    pil_image = Image.open(os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage", os.path.basename(image_file)))
    resized_image = pil_image.resize((64, 64), Image.Resampling.LANCZOS)
    if has_transparency(resized_image):
        signage_frame = messagebox.askyesno("Signage","Would you like to add the signage background to your image?")
        if signage_frame:
            background = Image.open(os.path.join(path,"imgs","signage_blank.png"))
            resized_image = pil_image.resize((48, 48), Image.Resampling.LANCZOS)
            if background.mode != 'RGBA':
                background = background.convert('RGBA')
            if resized_image.mode != 'RGBA':
                resized_image = resized_image.convert('RGBA')

            alpha_mask = resized_image.split()[3]

            x = (background.width - resized_image.width) // 2
            y = (background.height - resized_image.height) // 2

            background.paste(resized_image, (x, y), alpha_mask)
            resized_image = background
    rgba_image_path = os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage", os.path.basename(image_file))
    resized_image.save(rgba_image_path)

    makevtf(os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage",os.path.basename(image_file)))
    os.rename(os.path.join(packagemanager.packagesdir, "resources", "BEE2", "signage",f"{os.path.splitext(os.path.basename(image_file))[0]}.vtf"),os.path.join(packagemanager.packagesdir, "resources", "materials", "signage", f"{os.path.splitext(os.path.basename(image_file))[0]}.vtf"))
    with open(os.path.join(packagemanager.packagesdir, "resources", "materials", "signage", f"{os.path.splitext(os.path.basename(image_file))[0]}.vmt"),"w") as vmt:
        vmt.write('"LightmappedGeneric"\n{\n$basetexture "signage/VTF.HERE"\n$surfaceprop glass\n$selfillum 1\n$decal 1\n%nopaint 1\n%noportal 1\n"%keywords" portal2\n}'.replace("VTF.HERE",f"{os.path.splitext(os.path.basename(image_file))[0]}.vtf"))



    newdata = [signage_data[0],signage_data[1],None,f"signage/{os.path.basename(image_file)}",f'signage/{f"{os.path.splitext(os.path.basename(image_file))[0]}.vtf"}']

    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "r") as file:
        file_content = file.read()

    updated_content = file_content.replace(get_signage_block(signage_data), get_signage_block(newdata))

    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "w") as file:
        file.write(updated_content)

    assetmanager.format_file(os.path.join(packagemanager.packagesdir, "info.txt"))

    loadsign()

def on_hover_sign(event, button_name):
    status_bar3.config(text=f"{button_name[1]}")

def on_leave_sign(event):
    status_bar3.config(text="")

def loadsign():
    global sign_frame
    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "r") as file:
        signagefile = assetmanager.find_blocks(file.read(), '"Signage"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')

    if 'sign_frame' in globals():
        for widget in sign_frame.winfo_children():
            widget.destroy()
    else:
        # If sign_frame does not exist, create it
        sign_frame = tk.Frame(signage)
        sign_frame.pack(fill='both', expand=True)

    if not signagefile:
        return

    signagedict = {}

    for index,signageitem in enumerate(signagefile):
        signageitem = signageitem.replace("\t","").split("\n")

        id = signageitem[2].replace('"ID" "',"").replace('"',"")
        name = signageitem[3].replace('"Name" "',"").replace('"',"")
        icon = signageitem[8].replace('"icon"    "',"").replace('"',"")
        if '"Secondary" ' in signageitem[4]:
            sec = signageitem[4].replace('"Secondary" ',"").replace('"',"")
        else:
            sec = None
        if icon == r"{":
            icon = signageitem[9].replace('"icon"    "',"").replace('"',"")
            overlay = signageitem[10].replace('"overlay" "',"").replace('"',"")
        else:
            overlay = signageitem[9].replace('"overlay" "',"").replace('"',"")

        signagedict[index] = [id,name,sec,icon,overlay]

    num_rows = ceil((len(signagedict) + 1) / 4)

    for index, (id, name, sec, icon, overlay) in enumerate(signagedict.values()):
        row = index // 4
        col = index % 4

        try:
            icon_path = os.path.join(packagemanager.packagesdir, "resources", "BEE2", icon)
            pil_image = Image.open(icon_path)
        except FileNotFoundError:
            icon_path = os.path.join(path,"imgs","error.png")
            pil_image = Image.open(icon_path)
        resized_image = pil_image.resize((64, 64), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)

        button = tk.Button(sign_frame, image=tk_image, highlightthickness=0, 
                           command=lambda data=(id, name, sec, icon, overlay): chooseimage(data))
        button.bind('<Button-3>', lambda event, data=(id, name, sec, icon, overlay): delete_sign(event, data))
        button.image = tk_image
        button.bind("<Enter>", lambda event, data=(id, name, sec, icon, overlay): on_hover_sign(event, data))
        button.bind("<Leave>", on_leave_sign)
        button.grid(row=row, column=col, padx=5, pady=5)

    sign_frame.grid_propagate(False)
    sign_frame.config(width=4 * 70, height=num_rows * 70)

loadsign()

#Styles AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
stylemenu = tk.Toplevel()
stylemenu.title("Styles")
stylemenu.geometry(f"304x500")
stylemenu.resizable(False,False)
stylemenu.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))
stylemenu.protocol("WM_DELETE_WINDOW", stylemenu.withdraw)
status_bar_frame4 = ttk.Frame(stylemenu)
status_bar_frame4.pack(side=tk.BOTTOM, fill=tk.X)
status_bar4 = ttk.Label(status_bar_frame4, text="", relief=tk.SUNKEN, anchor=tk.W)
status_bar4.pack(fill=tk.X)

styledict = {}

def choose_style(data):
    print(data)

def on_hover_style(event, index):
    status_bar4.config(text=f"{styledict[index]['Name']}")

def on_leave_style(event):
    status_bar4.config(text="")

def loadstyle():
    global style_frame
    global styledict

    # Define a regex pattern to capture "Style" blocks
    style_pattern = r'"Style"\s*\{(.*?(?:\{.*?\}.*?)*?)\n\s*\}'

    style_file_path = os.path.join(packagemanager.packagesdir, "info.txt")
    if not os.path.exists(style_file_path):
        print(f"File not found: {style_file_path}")
        return

    with open(style_file_path, "r") as file:
        content = file.read()

    style_blocks = re.findall(style_pattern, content, re.DOTALL)

    if 'style_frame' in globals():
        for widget in style_frame.winfo_children():
            widget.destroy()
    else:
        style_frame = tk.Frame(stylemenu)
        style_frame.pack(fill='both', expand=True)

    if not style_blocks:
        print("No style blocks found")
        return

    styledict = {}

    for index, block in enumerate(style_blocks):
        lines = block.split("\n")
        style_data = {
            'ID': get_value(lines, '"ID"'),
            'Name': get_value(lines, '"Name"'),
            'Folder': get_value(lines, '"Folder"'),
            'Icon': get_value(lines, '"Icon"'),
            'IconLarge': get_value(lines, '"IconLarge"'),
            'Group': get_value(lines, '"Group"'),
            'ShortName': get_value(lines, '"ShortName"'),
            'Base': get_value(lines, '"Base"')
        }
        styledict[index] = style_data

    for index, (id, name, folder, icon, icon_large, group, short_name, base) in enumerate(styledict.values()):
        row = index // 4
        col = index % 4

        try:
            icon_path = os.path.join(packagemanager.packagesdir, "resources", "BEE2", styledict[index]['Icon'])
            print(icon_path)
            pil_image = Image.open(icon_path)
        except FileNotFoundError:
            icon_path = os.path.join(path, "imgs", "error.png")
            pil_image = Image.open(icon_path)
        
        resized_image = pil_image.resize((64, 64), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)

        button_data = (id, name, folder, icon, icon_large, group, short_name, base)
        button = tk.Button(style_frame, image=tk_image, highlightthickness=0,
                        command=choose_style(button_data))
        button.image = tk_image
        button.bind("<Enter>", lambda event, index=index: on_hover_style(event, index))
        button.bind("<Leave>", on_leave_style)
        button.grid(row=row, column=col, padx=5, pady=5)

    style_frame.grid_propagate(False)
    # Adjust the width and height as needed
    style_frame.config(width=4 * 70, height=(len(styledict) // 4 + 1) * 70)

def get_value(lines, key):
    for line in lines:
        if key in line:
            parts = line.split('"')
            if len(parts) > 2:
                return parts[-2].strip()
    return ""

loadstyle()

log.loginfo(f'Started UI ({round(time.time() - trn,2)}s)')
on_click(0, 0, first_item_frame, ctrl=False)
firsttime = 1
itemmenu.mainloop()


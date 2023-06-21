import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk, ImageColor
import zipfile
import ast
import assetmanager
import log
import numpy as np
from random import choice
from srctools import Property
import traceback
import winreg
import requests
import re
import packagemanager
from tkinter import filedialog,messagebox
import os
import pyperclip
import shutil
import sys

def intui():
    os.system('cls' if os.name == 'nt' else 'clear')

    def finditemkey():
        itemcall = selected[1:]
        for x in itemsdict:
            if itemcall in itemsdict[x][1]:
                return x

    def findp2dir():
        """
        Return a tuple with with all the steam libraries that it can find. The first library in the tuple will always be the main Steam directory.

        First checks the registry key for SteamPath, and if it can't find it, the path will be prompted to the user.
        
        CODE WAS FROM https://github.com/DarviL82/HAInstaller/blob/main/src/HAInstaller.py LINE 200:253 AND WAS EDITED
        """

        log.loginfo("Finding Steam")

        try:
            # Read the SteamPath registry key
            hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\Valve\Steam")
            folder = winreg.QueryValueEx(hkey, "SteamPath")[0]
            winreg.CloseKey(hkey)
        except Exception:
            messagebox.showerror("Error","Could not find steam path!\nPlease input your steam path.")
            folder = filedialog.askdirectory()

        # Continue asking for path until it is valid
        while not os.path.isdir(folder):
            messagebox.showerror("Error","Could not find steam path!\nPlease input your steam path.")
            folder = filedialog.askdirectory()

        steamlibs: list[str] = [folder.lower()]

        # Find other steam libraries (thanks TeamSpen)
        try:
            with open(os.path.join(folder, "steamapps/libraryfolders.vdf")) as file:
                conf = Property.parse(file)
        except FileNotFoundError:
            pass
        else:
            for prop in conf.find_key("LibraryFolders"):
                if prop.name.isdigit():
                    lib = prop[0].value
                    if os.path.isdir(os.path.join(lib, "steamapps/common")):
                        steamlibs.append(lib.replace("\\", "/").lower())

        # remove possible duplicates
        steamlibs = tuple(set(steamlibs))

        if len(steamlibs) > 1:
            log.loginfo("Found steam directories")
        else:
            log.loginfo(f"Found steam directories {folder}")

        #convert to p2 dir
        modified_paths = [path + '/steamapps/common' for path in steamlibs]

        p2dir = None

        for dir in modified_paths:
            if os.path.isfile(os.path.join(dir,"Portal 2","portal2.exe")):
                p2dir = os.path.join(dir,"Portal 2")

        return p2dir

    global name_variable,desc_variable
    def updatainfo():
        itemkey = finditemkey()
        global name_variable,desc_variable
        selected = listbox.get(listbox.curselection())[1:]
        if len(selected) <= 17:
            newvar = selected
        else:
            newvar = selected[:17] + "..."
        if itemsdict[itemkey][3] == True:
            name_variable.set("[D] " + newvar)
        else:
            name_variable.set(newvar)
        desc_variable.set(getdescription())

    def forcedelete(dir):
        while os.path.isdir(dir):
            shutil.rmtree(dir, ignore_errors=True)


    def on_select(event):
        global selected
        # Get the selected item from the listbox
        selected = listbox.get(listbox.curselection())[1:]
        itemkey = finditemkey()
        if len(selected) <= 17:
            newvar = selected
        else:
            newvar = selected[:17] + "..."
        if itemsdict[itemkey][3] == True:
            name_variable.set("[D] " + newvar)
        else:
            name_variable.set(newvar)
        desc_variable.set(getdescription())
        log.loginfo(f"Selected = {selected}")

    if os.path.basename(sys.executable) == "python.exe":
        path = __file__.replace(os.path.basename(__file__),"")
        log.loginfo(f"Local Path is __file__")
    else:
        path = sys.executable.replace(os.path.basename(sys.executable),"")
        log.loginfo(f"Local Path is sys.executable")

    imgdir = os.path.join(path,"imgs/")

    def use_image(name_img,wxh):
        img = Image.open(os.path.join(imgdir,name_img))
        return img.resize(wxh)

    def convert_color(image, old_color, new_color):
        # Convert the image to RGB mode
        image = image.convert("RGB")
        
        # Get the width and height of the image
        width, height = image.size
        
        # Loop through each pixel of the image
        for x in range(width):
            for y in range(height):
                # Get the RGB values of the pixel
                r, g, b = image.getpixel((x, y))
                
                # Convert the RGB values to hex format
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                
                # If the pixel color matches the old_color, replace it with the new_color
                if hex_color == old_color:
                    r, g, b = new_color[1:3], new_color[3:5], new_color[5:7]
                    image.putpixel((x, y), (int(r, 16), int(g, 16), int(b, 16)))
        return image

    def cleandir(folder):
        for root, dirs, files in os.walk(folder, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    log.loginfo(f"Removed empty directory: {dir_path}")
                except OSError:
                    # Directory is not empty
                    pass
    global theme1
    global theme2
    global theme3
    global theme4

    global dtheme1
    global ltheme1
    theme1 = "#878787"
    theme2 = "#232323"
    theme3 = "#4d4d4d"
    theme4 = "#878787"

    ltheme1 = "#474747"
    ltheme2 = "#dedede"
    ltheme3 = "#7a7a7a"
    ltheme4 = "#FFFFFF"

    dtheme1 = "#878787"
    dtheme2 = "#232323"
    dtheme3 = "#4d4d4d"
    dtheme4 = "#878787"

    items = []
    editor = []
    id = []
    global itemsdict


    dbtnmappings = [
        (dtheme1, dtheme3),
        (dtheme2, dtheme2),
        (dtheme3, dtheme1)
    ]

    lbtnmappings = [
        (dtheme1, ltheme3),
        (dtheme2, ltheme2),
        (dtheme3, ltheme1),
    ]

    def themefyimg(image,dmapping,lmapping):
        global theme1, dtheme1
        if theme1 == dtheme1:
            for original_color, theme_color in dmapping:
                image = convert_color(image, original_color, theme_color)
        else:
            for original_color, theme_color in lmapping:
                image = convert_color(image, original_color, theme_color)
        return image

    #Refresh Package
    def refreshpack():
        log.loginfo("Refreshing package!")
        global itemsdict
        items.clear()
        editor.clear()
        id.clear()
        with open(os.path.join(path,"config.bpe"),"r") as config:
            filepath = config.read()
            itemsdict = packagemanager.readfile(filepath)
        for x in range(len(itemsdict) - 1):
            appendthis = itemsdict[x]
            items.append(appendthis[1])
            editor.append(appendthis[2])
            id.append(appendthis[0])
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, " " + item)
        if items:
            pass
        else:
            messagebox.showerror("Error","No items in package!\nPlease select another package.")
            changepack()
        log.loginfo("Package Reloaded!")

    #Change package
    def changepack():
        log.loginfo("Changing package")
        filepath = filedialog.askopenfilename()
        if filepath:
            path2 = filepath
            try:
                shutil.rmtree(os.path.join(path,"packages"), ignore_errors=True)
                try:
                    os.makedirs(os.path.join(path,"packages"))
                except:
                    log.logwarn("Packages folder not fully removed!")
                with zipfile.ZipFile(path2, 'r') as zip_ref:
                    txtfile = zip_ref.open('info.txt', 'r')
                    txtlist = txtfile.read().decode().split("\n")
                if "//" in txtlist[0]:
                    with open(os.path.join(path,"config.bpe"),"w") as config:
                        config.write(path2)
                        log.loginfo(f"Changing to {os.path.basename(path2)}")
                    name_variable.set("")
                    refreshpack()
                else:
                    result = messagebox.askyesno("Warning", "Not a BeePKG package!\nWould you like to open this anyways?\nYou may encounter errors by doing this.")
                    if result == True:
                        with open(os.path.join(path,"config.bpe"),"w") as config:
                            config.write(path2)
                            log.loginfo(f"Changing to {os.path.basename(path2)}")
                        name_variable.set("")
                        refreshpack()
            except Exception as error:
                pyperclip.copy(traceback.format_exc())
                messagebox.showerror("Error", traceback.format_exc(), detail= "This has been copied to the clipboard.")

    with open(os.path.join(path,"config.bpe"),"r") as config:
        filepath = config.read()
        itemsdict = packagemanager.readfile(filepath)
    for x in range(len(itemsdict) - 1):
        appendthis = itemsdict[x]
        items.append(appendthis[1])
        editor.append(appendthis[2])
        id.append(appendthis[0])
    global typenum
    global typevar
    global menu
    global disablebutton
    global rmbutton
    global vbspbutton
    global listbox
    global inputbutton
    global autobutton
    global menu_button
    global menu_icon
    global debugbutton
    global frame
    global buttone
    global desc_box
    global name_box
    global button
    global iopopup
    global selected
    global popup
    typevar = "Add Button Type"
    typenum = 1
    popup = None
    iopopup = None
    global selected
    global root
    global fuckyouforspammingbutton
    selected = None
    fuckyouforspammingbutton = 0
    root = tk.Tk()
    root.resizable(False, False)
    root.geometry("800x600+300+200")
    root.configure(bg=theme2)
    root.title("Beemod Package Editor (BPE) V.2")
    root.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

    # Create a list of items

    # Create a tk.Frame to hold the listbox
    frame = tk.Frame(root, bg=theme2,padx=10,pady=10)
    frame.grid(column=0, row=0)

    # Create a tk.Listbox
    listbox = tk.Listbox(frame, height=36, width=50, bg=theme2,fg=theme1, bd=0, highlightthickness=0)
    listbox.grid(column=0, row=0)

    # Insert the items into the listbox
    for item in items:
        listbox.insert(tk.END, " " + item)

    # Add a scrollbar to the frame
    scrollbar = tk.Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listbox.yview)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(bg=theme2)
    scrollbar.grid(column=1, row=0, sticky="ns")
    # Bind the listbox to the on_select function
    listbox.bind("<<ListboxSelect>>", on_select)

    #Information board
    name_variable = tk.StringVar()
    selected = choice(items)
    name_variable.set(selected)
    name_box = tk.Label(root, textvariable=name_variable,bg=theme2,fg=theme1, anchor="center",width=17,bd=0,font=("Arial", 20, "bold"))
    name_box.place(x=410, y=50)
    #Name of item

    #Item description

    def getdescription():
        key = finditemkey()
        with open(os.path.join(packagemanager.packagesdir, "items", itemsdict[key][2], "properties.txt")) as file:
            file_content = file.read()  # Read the file content as a string
            blocks = assetmanager.find_blocks(file_content, '"Description" ', pattern=r'({key}\s*\{{(?:.*?\n)*?\s*\}})')
            if blocks is not None:
                blocks = ''.join(blocks)

                # Use regular expressions to extract the description text
                matches = re.findall(r'"" "(.*?)"', blocks)
                max_lines = 3
                limited_matches = matches[:max_lines]
                readable_string = '\n'.join(limited_matches)
                if len(matches) > max_lines:
                    readable_string += '\n...'
                return readable_string

            else:
                matches = re.findall(r'"Description"\s+"(.*?)"', file_content)
                if matches:
                    readable_string = '\n'.join(matches)
                    limit = 60
                    if len(readable_string) > limit:
                        readable_string = readable_string[:limit - 3] + "..."
                    return readable_string

                else:
                    return None

    desc_variable = tk.StringVar()
    desc_variable.set(getdescription())
    desc_box = tk.Label(root, textvariable=desc_variable,bg=theme2,fg=theme1, anchor="w",width=50,bd=0,font=("Arial", 8))
    desc_box.place(x=410, y=100)
    def showdesc(event):
        key = finditemkey()
        with open(os.path.join(packagemanager.packagesdir, "items", itemsdict[key][2], "properties.txt")) as file:
            file_content = file.read()  # Read the file content as a string
            blocks = assetmanager.find_blocks(file_content, '"Description" ', pattern=r'({key}\s*\{{(?:.*?\n)*?\s*\}})')
            if blocks is not None:
                blocks = ''.join(blocks)

                # Use regular expressions to extract the description text
                matches = re.findall(r'"" "(.*?)"', blocks)
                readable_string = '\n'.join(matches)
                messagebox.showinfo("Description", readable_string)

            else:
                matches = re.findall(r'"Description"\s+"(.*?)"', file_content)
                if matches:
                    readable_string = '\n'.join(matches)
                    messagebox.showinfo("Description", readable_string)

                else:
                    messagebox.showinfo("Description", "None")

    desc_box.bind("<Button-1>", showdesc)

    #Autopack 
    def autopack():
        log.loginfo("Running Autopack")
        global selected
        global itemsdict
        global fuckyouforspammingbutton
        if not selected:
            pass

        else:
            try:
                autobutton.config(state="disable")
                itemkey = finditemkey()
                #Get path to instances (Looking in vbsp_config, and editoritems)
                lookfor = []
                packagesdir = os.path.join(path,"packages")
                #Search editoritems.txt
                with open(os.path.join(packagesdir,"items",itemsdict[itemkey][2],"editoritems.txt")) as file:
                    editoritemslines = file.read().replace("\t","").split("\n")
                for x in editoritemslines:
                    if '"NAME"' in x.upper() and "INSTANCES" in x.upper():
                        lookfor.append(x.replace('"Name"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
                #Search vbsp_config (if it exists)
                if os.path.isfile(os.path.join(packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")) == True:
                    with open(os.path.join(packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")) as file:
                        editoritemslines = file.read().replace("\t","").split("\n")
                    for x in editoritemslines:
                        if '"ADDOVERLAY"' in x.upper() and "INSTANCES" in x.upper():
                            lookfor.append(x.replace('"AddOverlay"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
                        if '"CHANGEINSTANCE"' in x.upper() and "INSTANCES" in x.upper():
                            lookfor.append(x.replace('"ChangeInstance"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
                #Once we have gotten the instances we want to check if it actually exists or not
                instancelist = []
                for x in list(set(lookfor)):
                    if os.path.isfile(os.path.join(packagesdir,"resources",x)) == True:
                        instancelist.append(x)
                packlist = []
                for instance in instancelist:
                    packdict = packagemanager.readvmf(os.path.join(packagesdir,"resources",instance),"MODEL,MATERIAL,SOUND,SCRIPT")
                    for key, value in packdict.items():
                        if value:
                            for sublist in value:
                                packlist.append(sublist.lower())
                #Checks if the materials are base or not if it is we remove them from the list
                
                #Before doing anything with packing we will check the model files for material dependencies.
                
                p2 = findp2dir()
                dependentassets = []
                packlist = list(set(packlist))

                for assets in packlist:
                    if assets[:6] == "models":
                        #If this is a model file we find the dependent materials.
                        for deassets in assetmanager.finedepen(assets,p2):
                            dependentassets.append(deassets)
                            log.loginfo(f'{os.path.splitext(os.path.basename(assets + ".vtf"))[0]} has dependent assets! {deassets}')
                
                #combine the 2 lists
                packlist.extend(dependentassets)
                #Remove duplicate
                packlist = list(set(packlist))

                #Getting the list from an "api" because its too long
                baseassets = requests.get("https://versioncontrol.areng123.repl.co/data/baseassets")
                baseassets = baseassets.text.replace(" ","").replace("'","").split(",")
                for x in range(len(packlist)):
                    if os.path.splitext(os.path.basename(packlist[x]))[0].upper() in baseassets:
                        packlist[x] = "PACKER_IGNORE"

                log.loginfo(f"Packages that needs to be packed: {packlist}")

                #Packing!
                errors = []
                counterv = 0
                packedvar = 0
                for asset in packlist:
                    if asset != "PACKER_IGNORE":
                        log.loginfo(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} is an actual asset that needs to be packed!')
                        if asset[:8] == "material":
                            log.loginfo(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} is a material!')
                            #Material packing!
                            #Making folders
                            packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + ".vtf").replace(os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf")),""))
                            if os.path.isfile( os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf")))) != True and os.path.isfile( os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt")))) != True:
                                if os.path.isdir(packagematpath) == False:
                                    os.makedirs(packagematpath.lower())
                                #Finding the .vtf and the .vmt
                                counter = 0
                                for x in range(999):
                                    if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt")) == True:
                                        log.loginfo(f"Found asset in portal2_dlc{x}")
                                        try:
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt"))))
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".vtf")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".vtf"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf"))))
                                            log.loginfo(f"Sucesfully moved assets!")
                                            break
                                        except:
                                            log.logerror(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} We could not move this because it was causing an error.')
                                            log.loginfo(f'Undoing packing of {os.path.splitext(os.path.basename(asset + ".vtf"))[0]}!')
                                            try:
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt")))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt"))))
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf")))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf"))))
                                            except:
                                                pass
                                            cleandir(packagemanager.packagesdir)
                                            counter += 1000
                                            break
                                    else:
                                        log.logerror(f'Could not find {os.path.splitext(os.path.basename(asset + ".vtf"))[0]} in {os.path.join(p2,f"portal2_dlc{x}",asset + ".vtf")}')
                                    counter += 1
                                if counter >= 999:
                                    errors.append(asset.lower())
                            else:
                                packedvar += 1
                        if asset[:6] == "models":
                            log.loginfo(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} is a model!')
                            #Model packing!
                            #Making folders
                            asset = asset.replace(".mdl","")
                            #Fixing up asset before entering
                            packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + ".mdl").replace(os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")),""))
                            if os.path.isfile( os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))) != True and os.path.isfile( os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy")))) != True and os.path.isfile(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtx")))) != True and os.path.isfile( os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd")))) != True:
                                if os.path.isdir(packagematpath) == False:
                                    os.makedirs(packagematpath.lower())
                                #Finding the .vtf and the .vmt
                                counter = 0
                                for x in range(999):
                                    if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")) == True:
                                        log.loginfo(f"Found asset in portal2_dlc{x}")
                                        try:
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl"))))
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".vvd")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".vvd"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd"))))
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".dx90.vtx")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".dx90.vtx")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".dx90.vtx"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".dx90.vtx"))))
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".phy")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".phy"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy"))))
                                            log.loginfo(f"Sucesfully moved assets!")
                                            break
                                        except:
                                            log.logerror(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} We could not move this because it was causing an error.')
                                            log.loginfo(f'Undoing packing of {os.path.splitext(os.path.basename(asset + ".vtf"))[0]}!')
                                            try:
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl"))))
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd")))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd"))))
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".dx90.vtx")))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".dx90.vtx"))))
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy")))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy"))))
                                            except:
                                                pass
                                            cleandir(packagemanager.packagesdir)
                                            counter += 1000
                                            break
                                    else:
                                        log.logerror(f'Could not find {os.path.splitext(os.path.basename(asset + ".vtf"))[0]} in {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")}')
                                    counter += 1
                                if counter >= 999:
                                    errors.append(asset.lower())
                            else:
                                packedvar += 1
                        if asset[:6] == "message":
                            log.loginfo(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} is a sound!')
                            #Sound packing!
                            #Making folders
                            extension = os.path.splitext(os.path.basename(asset))[1]
                            packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + extension).replace(os.path.basename(os.path.join(packagesdir,"resources",asset + extension)),""))
                            if os.path.isfile(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension)))) != True:
                                if os.path.isdir(packagematpath) == False:
                                    os.makedirs(packagematpath.lower())
                                #Finding the .vtf and the .vmt
                                counter = 0
                                for x in range(999):
                                    if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + extension)) == True:
                                        log.loginfo(f"Found asset in portal2_dlc{x}")
                                        try:
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + extension), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension))))
                                            log.loginfo(f"Sucesfully moved assets!")
                                            break
                                        except:
                                            log.logerror(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} We could not move this because it was causing an error.')
                                            log.loginfo(f'Undoing packing of {os.path.splitext(os.path.basename(asset + ".vtf"))[0]}!')
                                            try:
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension)))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension))))
                                            except:
                                                pass
                                            cleandir(packagemanager.packagesdir)
                                            counter += 1000
                                            break
                                    else:
                                        log.logerror(f'Could not find {os.path.splitext(os.path.basename(asset + ".vtf"))[0]} in {os.path.join(p2,f"portal2_dlc{x}",asset + extension)}')
                                    counter += 1
                                if counter >= 999:
                                    errors.append(asset.lower())
                            else:
                                packedvar += 1
                        if asset[:6] == "scripts":
                            log.loginfo(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} is a script!')
                            #Sript packing!
                            #Making folders
                            extension = ".nut"
                            packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + extension).replace(os.path.basename(os.path.join(packagesdir,"resources",asset + extension)),""))
                            if os.path.isfile(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension)))) != True:
                                if os.path.isdir(packagematpath) == False:
                                    os.makedirs(packagematpath.lower())
                                #Finding the .vtf and the .vmt
                                counter = 0
                                for x in range(999):
                                    if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + extension)) == True:
                                        log.loginfo(f"Found asset in portal2_dlc{x}")
                                        try:
                                            log.loginfo(f'Copying asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + extension), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension))))
                                            log.loginfo(f"Sucesfully moved assets!")
                                            break
                                        except:
                                            log.logerror(f'{os.path.splitext(os.path.basename(asset + ".vtf"))[0]} We could not move this because it was causing an error.')
                                            log.loginfo(f'Undoing packing of {os.path.splitext(os.path.basename(asset + ".vtf"))[0]}!')
                                            try:
                                                log.loginfo(f'Removing asset: {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension)))}')
                                                os.remove(os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension))))
                                            except:
                                                pass
                                            cleandir(packagemanager.packagesdir)
                                            counter += 1000
                                            break
                                    else:
                                        log.logerror(f'Could not find {os.path.splitext(os.path.basename(asset + ".vtf"))[0]} in {os.path.join(p2,f"portal2_dlc{x}",asset + extension)}')
                                    counter += 1
                                if counter >= 999:
                                    errors.append(asset.lower())
                            else:
                                packedvar += 1
                    else:
                        counterv += 1
                log.loginfo(f"End values: ErrorsV {errors}, CounterV {counterv}, Packedvar {packedvar}")
                if errors:
                    messagebox.showwarning("Warning!","----------------------------------------\n" + '\n'.join(str(i) for i in errors) + "\n----------------------------------------\n\nWe could not find the assets in your portal 2 dlc folders.\nIf you belive this to be an error, please contact Areng#0001 on discord. or make an issue on the github.\n(These files were not packed)")
                elif counterv == len(packlist):
                    messagebox.showinfo("Info",f"There were no assets to pack for {selected}!\nThis means this item uses base assets.")
                elif packedvar == len(packlist):
                    messagebox.showinfo("Info",f"Assets are already packed in {selected}!")
                else:
                    messagebox.showinfo("Info",f"Assets sucessfully packed for {selected}!")
                autobutton.config(state="normal")
            except Exception as error:
                pyperclip.copy(traceback.format_exc())
                messagebox.showerror("Error", traceback.format_exc(), detail= "This has been copied to the clipboard.")
                autobutton.config(state="normal")


    def changetheme():
        global theme1
        global root
        global menu
        global vbspbutton
        global inputbutton
        global autobutton
        global debugbutton
        global menu_button
        global menu_icon
        global frame
        global popup
        global rmbutton
        global disablebutton
        global iopopup
        global text
        global name_box
        global listbox
        global desc_box
        global buttone
        global theme2
        global theme3
        global theme4
        if theme1 == "#878787":
            log.loginfo("Changing to light mode")
            theme1 = ltheme1
            theme2 = ltheme2
            theme3 = ltheme3
            theme4 = ltheme4
            menu_icon = ImageTk.PhotoImage(use_image("menul.png",(20,20)))
        else:
            log.loginfo("Changing to dark mode")
            theme1 = dtheme1
            theme2 = dtheme2
            theme3 = dtheme3
            theme4 = dtheme4
            menu_icon = ImageTk.PhotoImage(use_image("menu.png",(20,20)))
        buttons = [vbspbutton,inputbutton,autobutton,debugbutton,buttone,rmbutton,disablebutton]
        for button in buttons:
            button.configure(bg=theme3,fg=theme4)
        name_box.configure(bg=theme2,fg=theme1)
        listbox.configure(bg=theme2,fg=theme1)
        menu.configure(bg=theme2,fg=theme1)
        menu.configure(activebackground=theme1, activeforeground=theme2)
        menu_button.configure(image=menu_icon)
        frame.configure(bg=theme2)
        desc_box.configure(bg=theme2,fg=theme1)
        root.configure(bg=theme2)
        if popup:
            popup.configure(bg=theme2)
            popup.update_idletasks()
        if iopopup:
            iopopup.configure(bg=theme2)
            iopopup.update_idletasks()
        root.update_idletasks()



    #Utils
    menu_icon = ImageTk.PhotoImage(use_image("menu.png",(20,20)))
    menu_button = tk.Button(root, image=menu_icon, width=16, height=16, bd=0)
    menu_button.place(x=770, y=10)
    menu = tk.Menu(root, tearoff=0, bg=theme2,fg=theme1,bd=0)
    menu.add_command(label="Reload Packages", command=refreshpack, activebackground=theme1, activeforeground=theme2)
    menu.add_command(label="Change Package", command=changepack,activebackground=theme1, activeforeground=theme2)
    menu.add_separator()
    menu.add_command(label="Change Theme", command=changetheme,activebackground=theme1, activeforeground=theme2)

    def display_menu(event):
        menu.post(event.x_root, event.y_root)
    menu_button.bind("<Button-1>", display_menu)


    #Buttons
    autobutton = tk.Button(root, text="Autopacker",command=autopack,font=("Arial", 11) ,bd=0,bg=theme3,fg=theme4)
    autobutton.place(width=128, height=32,x=610, y=200)

    #Leak checker

    def ioedit():
        global iopopup
        log.loginfo("Running ioedit")
        if not selected:
            messagebox.showerror("Error","Please select an item first!")
            return 
        itemkey = finditemkey()

        #Get path to instances (Looking in vbsp_config, and editoritems)
        #Get VMFs
        lookfor = []
        packagesdir = os.path.join(path,"packages")
        #Search editoritems.txt
        log.loginfo("Finding VMFs")
        with open(os.path.join(packagesdir,"items",itemsdict[itemkey][2],"editoritems.txt")) as file:
            editoritemslines = file.read().replace("\t","").split("\n")
        for x in editoritemslines:
            if '"NAME"' in x.upper() and "INSTANCES" in x.upper():
                lookfor.append(x.replace('"Name"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
        #Search vbsp_config (if it exists)
        if os.path.isfile(os.path.join(packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")) == True:
            with open(os.path.join(packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")) as file:
                editoritemslines = file.read().replace("\t","").split("\n")
            for x in editoritemslines:
                if '"ADDOVERLAY"' in x.upper() and "INSTANCES" in x.upper():
                    lookfor.append(x.replace('"AddOverlay"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
                if '"CHANGEINSTANCE"' in x.upper() and "INSTANCES" in x.upper():
                    lookfor.append(x.replace('"ChangeInstance"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
        #Once we have gotten the instances we want to check if it actually exists or not
        instancelist = []
        for x in list(set(lookfor)):
            if os.path.isfile(os.path.join(packagesdir,"resources",x)) == True:
                instancelist.append(os.path.join(packagesdir,"resources",x))

        log.loginfo("Reading VMFs")
        entitydict = {}
        for instance in instancelist:
            with open(instance, "r") as vmf:
                file_content = vmf.read()
                entityblocks = assetmanager.find_blocks(file_content, "entity")
                if entityblocks:
                    for block in entityblocks:
                        try:
                            pattern = re.compile(r'"targetname"\s*"([^"]*)"')
                            match = pattern.search(block)
                            classpattern = re.compile(r'"classname"\s*"([^"]*)"')
                            classmatch = classpattern.search(block)
                            entitydict[match.group(1)] = classmatch.group(1)
                        except AttributeError:
                            pass  # Let Attribute Error pass because it means no text found.
                else:
                    print(f"No 'entity' blocks found in {instance}")
        print(entitydict)
        #Popup a UI to edit the inputs
        #Checks for entities if none handle it
        if entitydict:
            # Create the main window
            iopopup = tk.Toplevel()
            iopopup.title("Input / Output Editor")
            iopopup.geometry("384x256")
            iopopup.config(bg=theme2)
            iopopup.wm_iconbitmap(os.path.join(path, "imgs/", "bpe.ico"))

            entity_dict = entitydict
            entity_dict["----"] = ""
            entity_dict["Remove"] = "remove"

            # Create the dropdown widget for selecting an entity
            entityselected_option = tk.StringVar(iopopup)
            entityselected_option.set(next(iter(entity_dict.keys())))
            entitydropdown = tk.OptionMenu(iopopup, entityselected_option, *entity_dict.keys())
            entitydropdown.config(width=8, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            entitydropdown.place(x=60, y=32)

            # Create the dropdown widget for selecting a fire option
            fires = ast.literal_eval(assetmanager.getdata("data/input"))
            fireselected_option = tk.StringVar(iopopup)
            fireselected_option.set(fires[0])
            firedropdown = tk.OptionMenu(iopopup, fireselected_option, *fires)
            firedropdown.config(width=3, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            firedropdown.place(x=120, y=32)

            # Prevent newline
            def on_key_press(event):
                if event.keysym in ["Return", "KP_Enter", "Control-Return"]:
                    return "break"

            # Create the input text widget
            inputtxt = tk.Text(iopopup, height=1, width=8)
            inputtxt.bind("<Return>", on_key_press)
            inputtxt.bind("<KP_Enter>", on_key_press)
            inputtxt.bind("<Control-Return>", on_key_press)
            inputtxt.place(x=176, y=35)
            inputtxt.config(bg=theme2, fg=theme1)

            # Define the function to handle the Return and Control-Return events
            def on_key_press_delayer(event):
                # Allow the BackSpace and Delete keys
                if event.keysym in ["BackSpace", "Delete"]:
                    return
                # Allow digits and periods
                elif not event.char.isdigit() and event.char != ".":
                    # Allow the Control-x, Control-c, and Control-v shortcuts
                    if event.keysym not in ["Control_L", "Control_R", "c", "x", "v"]:
                        return "break"

            # Create the delay text widget
            delaytxt = tk.Text(iopopup, height=1, width=8)
            delaytxt.bind("<Return>", on_key_press_delayer)
            delaytxt.bind("<KP_Enter>", on_key_press_delayer)
            delaytxt.bind("<Control-Return>", on_key_press_delayer)
            delaytxt.bind("<Key>", on_key_press_delayer)
            delaytxt.place(x=236, y=35)
            delaytxt.config(bg=theme2, fg=theme1)

            # Load the inputinfo image
            inputinfoimg = ImageTk.PhotoImage(themefyimg(use_image("inputinfo.png", (244, 20)),dbtnmappings,lbtnmappings))

            # Create the inputinfo image label
            inputinfopng = tk.Label(iopopup, image=inputinfoimg, width=244, height=20, bd=0)
            inputinfopng.place(x=60, y=64)

            # Define the confirmadd function
            def confirmadd():
                # Compile input
                newdinput = f"{deentityselected_option.get()},{defireselected_option.get()},{deinputtxt.get('1.0', tk.END).strip()},{0 if not deinputtxt.get('1.0', tk.END).strip() else deinputtxt.get('1.0', tk.END)},-1"
                newainput = f"{entityselected_option.get()},{fireselected_option.get()},{inputtxt.get('1.0', tk.END).strip()},{0 if not deinputtxt.get('1.0', tk.END).strip() else deinputtxt.get('1.0', tk.END)},-1"
                yesno = messagebox.askyesno("Info", "Are you sure you want to replace the current input with the new input?")

                if yesno:
                    with open(os.path.join(packagesdir, "items", itemsdict[itemkey][2], "editoritems.txt")) as file:
                        content = file.read()
                        inputblocks = assetmanager.find_blocks(content.replace("\t","").replace(" ",""), '"Inputs"',r'{key}\s*{{[^}}]*}}\s*}}\s')

                        if inputblocks:
                            inputblock = inputblocks[0]
                        else:
                            inputblock = '"Inputs"\n{\n\n}'
                        if re.search(r'"BEE2"\s*{\s*}', inputblock):
                            # Handle case when the input block is present but empty
                            # You can add your logic or display an error message
                            print("Input block is present but empty")
                        else:
                            # Edit inputs
                            aoldinput = re.findall(r'"Enable_cmd""((?:[^\\"]|\\\\|\\")*)"', inputblock)
                            doldinput = re.findall(r'"Disable_cmd""((?:[^\\"]|\\\\|\\")*)"', inputblock)
                            if newainput == ",,,,-1":
                                ainput = aoldinput
                            elif entityselected_option.get() == "Remove":
                                ainput = ""
                            else:
                                ainput = newainput
                            if newdinput == ",,,,-1":
                                dinput = doldinput
                            elif deentityselected_option.get() == "Remove":
                                ainput = ""
                            else:
                                dinput = newdinput
                            bee2str = f'"Inputs"\n{{\n"BEE2"\n{{\n"Type" "AND"\n"Enable_cmd" "{ainput}"\n"Disable_cmd" "{dinput}"\n}}\n}}\n'
                            print(inputblock)
                            print(bee2str)
                            with open(os.path.join(packagesdir, "items", itemsdict[itemkey][2], "editoritems.txt"), "w") as file:
                                file.write(assetmanager.format_string(content.replace(" ","").replace("\t","").replace(inputblock,bee2str)))

            # Create the input activate button
            inputactivatebutton = tk.Button(iopopup, text="Add", command=confirmadd, font=("Arial", 8), bd=0, bg=theme3, fg=theme1,width=13)
            inputactivatebutton.place(x=198, y=112)

            def switchi_o():
                hideinput()
                showoutput()

            swapperbtn = tk.Button(iopopup, text="Output Editor", command=switchi_o, font=("Arial", 8), bd=0, bg=theme3, fg=theme1,width=13)
            swapperbtn.place(x=85, y=112)
            #declare the input stuff.

            #add the deactivate part
            # Create the dropdown widget for selecting an entity
            deentityselected_option = tk.StringVar(iopopup)
            deentityselected_option.set(next(iter(entity_dict.keys())))
            deentitydropdown = tk.OptionMenu(iopopup, deentityselected_option, *entity_dict.keys())
            deentitydropdown.config(width=8, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            deentitydropdown.place(x=60, y=192)

            # Create the dropdown widget for selecting a fire option
            defireselected_option = tk.StringVar(iopopup)
            defireselected_option.set(fires[0])
            defiredropdown = tk.OptionMenu(iopopup, defireselected_option, *fires)
            defiredropdown.config(width=3, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            defiredropdown.place(x=120, y=192)

            # Prevent newline
            def on_key_press(event):
                if event.keysym in ["Return", "KP_Enter", "Control-Return"]:
                    return "break"

            # Create the input text widget
            deinputtxt = tk.Text(iopopup, height=1, width=8)
            deinputtxt.bind("<Return>", on_key_press)
            deinputtxt.bind("<KP_Enter>", on_key_press)
            deinputtxt.bind("<Control-Return>", on_key_press)
            deinputtxt.place(x=176, y=195)
            deinputtxt.config(bg=theme2, fg=theme1)

            # Create the delay text widget
            dedelaytxt = tk.Text(iopopup, height=1, width=8)
            dedelaytxt.bind("<Return>", on_key_press_delayer)
            dedelaytxt.bind("<KP_Enter>", on_key_press_delayer)
            dedelaytxt.bind("<Control-Return>", on_key_press_delayer)
            dedelaytxt.bind("<Key>", on_key_press_delayer)
            dedelaytxt.place(x=236, y=195)
            dedelaytxt.config(bg=theme2, fg=theme1)


            # Create the inputinfo image label
            deinputinfopng = tk.Label(iopopup, image=inputinfoimg, width=244, height=20, bd=0)
            deinputinfopng.place(x=60, y=224)


            inputdeclaration = [inputactivatebutton, inputinfopng, inputtxt, delaytxt, firedropdown, entitydropdown, deinputinfopng, deinputtxt, dedelaytxt, defiredropdown, deentitydropdown,swapperbtn]
            inputinfo = []
            def hideinput():
                for button in inputdeclaration:
                    inputinfo.append(button.place_info())
                    button.place_forget()

            def showinput():
                hideinput()
                for index, button in enumerate(inputdeclaration):
                    button.place(inputinfo[index])

            #output
            outputentityselected_option = tk.StringVar(iopopup)
            outputentityselected_option.set(next(iter(entity_dict.keys())))
            outputentitydropdown = tk.OptionMenu(iopopup, entityselected_option, *entity_dict.keys())
            outputentitydropdown.config(width=8, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            outputentitydropdown.place(x=85, y=32)

            outfires = ast.literal_eval(assetmanager.getdata("data/output"))

            outputfireselected_option = tk.StringVar(iopopup)
            outputfireselected_option.set(outfires[0])
            outputfiredropdown = tk.OptionMenu(iopopup, outputfireselected_option, *outfires)
            outputfiredropdown.config(width=8, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            outputfiredropdown.place(x=198, y=32)



            doutputentityselected_option = tk.StringVar(iopopup)
            doutputentityselected_option.set(next(iter(entity_dict.keys())))
            doutputentitydropdown = tk.OptionMenu(iopopup, doutputentityselected_option, *entity_dict.keys())
            doutputentitydropdown.config(width=8, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            doutputentitydropdown.place(x=85, y=192)

            doutfires = ast.literal_eval(assetmanager.getdata("data/output"))

            doutputfireselected_option = tk.StringVar(iopopup)
            doutputfireselected_option.set(outfires[0])
            doutputfiredropdown = tk.OptionMenu(iopopup, doutputfireselected_option, *outfires)
            doutputfiredropdown.config(width=8, bd=0, bg=theme2, fg=theme1, highlightthickness=1, highlightcolor=theme1, highlightbackground=theme1)
            doutputfiredropdown.place(x=198, y=192)

            #Info
            outputinfoimg = ImageTk.PhotoImage(themefyimg(use_image("outputinfo.png", (200, 21)),dbtnmappings,lbtnmappings))

            outputinfopng1 = tk.Label(iopopup, image=outputinfoimg, width=200, height=21, bd=0)
            outputinfopng1.place(x=85, y=64)

            outputinfopng2 = tk.Label(iopopup, image=outputinfoimg, width=200, height=21, bd=0)
            outputinfopng2.place(x=85, y=224)

            def outconfirmadd():
                # Compile input
                newainput = f"instance:{outputentityselected_option.get()};{outputfireselected_option.get()}"
                newdinput = f"instance:{doutputentityselected_option.get()};{doutputfireselected_option.get()}"
                yesno = messagebox.askyesno("Info", "Are you sure you want to replace the current output with the new output?")
                if yesno:
                    with open(os.path.join(packagesdir, "items", itemsdict[itemkey][2], "editoritems.txt")) as file:
                        content = file.read()
                        inputblocks = assetmanager.find_blocks(content.replace("\t","").replace(" ",""), '"Outputs"',r'{key}\s*{{[^}}]*}}\s*}}\s')

                        if inputblocks:
                            inputblock = inputblocks[0]
                        else:
                            inputblock = '"Outputs"\n{\n\n}'
                        if re.search(r'"BEE2"\s*{\s*}', inputblock):
                            # Handle case when the input block is present but empty
                            # You can add your logic or display an error message
                            print("Input block is present but empty")
                        else:
                            # Edit inputs
                            aoldinput = re.findall(r'"out_activate""((?:[^\\"]|\\\\|\\")*)"', inputblock)
                            doldinput = re.findall(r'"out_deactivate""((?:[^\\"]|\\\\|\\")*)"', inputblock)
                            if newainput == "instance:;":
                                ainput = aoldinput
                            elif outputentityselected_option.get() == "Remove":
                                ainput = ""
                            else:
                                ainput = newainput
                            if newdinput == "instance:;":
                                dinput = doldinput
                            elif doutputentityselected_option.get() == "Remove":
                                ainput = ""
                            else:
                                dinput = newdinput
                            bee2str = f'"Outputs"\n{{\n"BEE2"\n{{\n"Type" "AND"\n"out_activate" "{ainput}"\n"out_deactivate" "{dinput}"\n}}\n}}\n'
                            print(inputblock)
                            print(bee2str)
                            with open(os.path.join(packagesdir, "items", itemsdict[itemkey][2], "editoritems.txt"), "w") as file:
                                file.write(assetmanager.format_string(content.replace(" ","").replace("\t","").replace(inputblock,bee2str)))

            outputactivatebutton = tk.Button(iopopup, text="Add", command=outconfirmadd, font=("Arial", 8), bd=0, bg=theme3, fg=theme1,width=13)
            outputactivatebutton.place(x=198, y=112)

            def switcho_i():
                hideoutput()
                showinput()

            swapperbtn = tk.Button(iopopup, text="Input Editor", command=switcho_i, font=("Arial", 8), bd=0, bg=theme3, fg=theme1,width=13)
            swapperbtn.place(x=85, y=112)

            outputdeclaration = [outputentitydropdown,outputfiredropdown,outputactivatebutton,swapperbtn,doutputentitydropdown,doutputfiredropdown,outputinfopng1,outputinfopng2]
            outputinfo = []

            def hideoutput():
                for button in outputdeclaration:
                    outputinfo.append(button.place_info())
                    button.place_forget()

            def showoutput():
                hideoutput()
                for index, button in enumerate(outputdeclaration):
                    button.place(outputinfo[index])

            hideoutput()

            # Start the main event loop
            iopopup.mainloop()
        else:
            messagebox.showerror("Error",f"{itemsdict[itemkey][1]}'s instance does not have a entity!\nThis may be because the entity does not have a name or this item has no entities")
        log.loginfo("Completed.")

    inputbutton = tk.Button(root, text="Connection Editor",command=ioedit,font=("Arial", 11) ,bd=0,bg=theme3,fg=theme4)
    inputbutton.place(width=128, height=32,x=610, y=250)

    #vbsp_editor

    def vbsp_editor():
        log.loginfo("Running vbsp editor")
        if not selected:
            messagebox.showerror("Error","Please select an item first!")
            return 
        itemkey = finditemkey()

        #Get vbsp_config contents if it exists
        pathtovbsp = os.path.join(packagemanager.packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")
        if os.path.isfile(pathtovbsp):
            with open(pathtovbsp) as vbsp:
                pass
        else:
            with open(pathtovbsp,"w") as vbsp:
                pass

        #ui stuff
        def open_file():
            global startinstance
            file_path = pathtovbsp
            # Format the file
            assetmanager.format_file(file_path)
            with open(file_path, "r") as file:
                file_content = file.read()
                text.delete("1.0", tk.END)
                text.insert("1.0", file_content)
                pattern = r'"Changeinstance"\s+"(.*?)"'
                startinstance = re.findall(pattern, file_content)
                print(startinstance)

        def add_text(text_widget, text):
            current_index = text_widget.index(tk.INSERT)
            text_widget.insert(current_index, text)

        def save_file():
            file_path = pathtovbsp
            assetmanager.format_file(file_path)
            if file_path is None:
                return
            data = text.get('1.0', 'end')

            # Remove unused instances
            pattern = r'"Changeinstance"\s+"(.*?)"'
            endinstance = re.findall(pattern, data)

            missing_items = [item for item in startinstance if item not in endinstance]
            choice = messagebox.askyesno("Missing Path","We detected there was some missing instances. Would you like to remove the instances from your package?")
            if choice:
                for item in missing_items:
                    log.logwarn(f"Removing {item} because it is removed so therefor it is useless.")
                    while os.path.isfile(os.path.join(packagemanager.packagesdir, "resources", "instances", "beepkg", itemsdict[itemkey][2], os.path.basename(item))):
                        os.remove(os.path.join(packagemanager.packagesdir, "resources", "instances", "beepkg", itemsdict[itemkey][2], os.path.basename(item)))
            with open(file_path, 'w') as file:
                file.write(data)

            log.loginfo("Changing editoritems.txt")
            #Check for cube type etc and add it to editoritems

            addthis = []

            if "$CUBE_TYPE 0" in data.upper():
                log.loginfo("Detected Cube Type")
                addthis.append(f'"CubeType"\n{{\n"DefaultValue" "0"\n"Index" "{len(addthis) + 2}"\n}}')
            if "$BUTTON_TYPE = 0" in data.upper():
                log.loginfo("Detected Button Type")
                addthis.append(f'"ButtonType"\n{{\n"DefaultValue" "0"\n"Index" "{len(addthis) + 2}"\n}}')
            if "$TIMER_DELAY == 3" in data.upper() and not '"BEE2_CUBE_COLORISER"' in data.upper():
                log.loginfo("Detected Timer Type")
                addthis.append(f'"TimerDelay"\n{{\n"DefaultValue" "0"\n"Index" "{len(addthis) + 2}"\n}}')
            elif '"BEE2_CUBE_COLORISER"' in data.upper() and "$TIMER_DELAY == 3" in data.upper():
                messagebox.showerror("Warning","You have cube colorizer and timer delay.\nCube Colorizer requires the use of the timer.")
                return
            if "$START_ENABLED = 1" in data.upper() or "$START_ENABLED = 0" in data.upper():
                log.loginfo("Detected Enabled Type")
                addthis.append(f'"StartEnabled"\n{{\n"DefaultValue" "0"\n"Index" "{len(addthis) + 2}"\n}}')
            if "$START_REVERSED = 1" in data.upper() or "$START_REVERSED = 0" in data.upper():
                log.loginfo("Detected Reversed Type")
                addthis.append(f'"StartReversed"\n{{\n"DefaultValue" "0"\n"Index" "{len(addthis) + 2}"\n}}')
            if '"BEE2_CUBE_COLORISER"' in data.upper():
                log.loginfo("Detected Colorizer")
                addthis.append(f'"TimerDelay"\n{{\n"DefaultValue" "0"\n"Index" "{len(addthis) + 2}"\n}}')

            if addthis:
                writethis = []
                for item in addthis:
                    writethis.append(item)
                bwritethis = '"ConnectionCount"\n{\n"DefaultValue"	"0"\n"Index"	"1"\n}'
                bwritethis += "\n" + "\n".join(writethis)
                writethis = bwritethis + "\n"

                with open(os.path.join(packagemanager.packagesdir, "items", itemsdict[itemkey][2], "editoritems.txt"),"r") as file:
                    content = file.read()
                properties = assetmanager.find_blocks(content.replace("\t", "").replace(" ", ""), '"Properties"', r'{key}\s*{{\s*((?:[^{{}}]|{{[^{{}}]*}})*)\s*}}')
                with open(os.path.join(packagemanager.packagesdir, "items", itemsdict[itemkey][2], "editoritems.txt"),"w") as file:
                    file.write(assetmanager.format_string(content.replace("\t","").replace(" ","").replace(properties[0].replace(" ",""),writethis.replace(" ",""))))

                messagebox.showinfo("Info", "File Saved Successfully")

        global popup
        global text

        #File management
        popup = tk.Toplevel()
        popup.title("Vbsp Editor")
        popup.geometry("600x400")
        popup.config(bg=theme2)
        popup.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

        text = tk.Text(popup, wrap='word', bg=theme2, fg=theme1, insertbackground=theme1, undo=True)
        text.pack(fill='both', expand=True)
        global button
        button = None

        def makeinstancepath():
            messagebox.showinfo("Info",f"Please select the instance file (.vmf)\nPackage files can be found at '{packagemanager.packagesdir}'")
            while True:
                file = filedialog.askopenfilename(filetypes=[("Valve Map Format", "*.vmf")],initialdir=os.path.join(path,"packages","resources","instances"))
                if packagemanager.packagesdir not in file:
                    os.rename(file,os.path.join(packagemanager.packagesdir,"resources","instances","beepkg",itemsdict[itemkey][2],os.path.basename(file)))
                    messagebox.showinfo("Info",f"{os.path.splitext(file)[0]} wasnt in your package so we added it.")
                if os.path.splitext(file)[1] == ".vmf":
                    break
                else:
                    messagebox.showerror("Error",f"{os.path.splitext(file)[0]} is not a .vmf file!")
            
            add_text(text,f'"Changeinstance" "instances/bee2/beepkg/{itemsdict[itemkey][0]}/{os.path.basename(file)}"')

        #Type maker
        def cubetypeadd():
            cubetypevbsp = assetmanager.getdata("vbsp/cube")

            #Replace vars
            cubetypevbsp = cubetypevbsp.replace("\t","").replace("vartochange(id)",f"<{itemsdict[itemkey][0].upper()}>")

            add_text(text,assetmanager.format_string(cubetypevbsp))

        def btntypeadd():
            cubetypevbsp = assetmanager.getdata("vbsp/button")

            #Replace vars
            cubetypevbsp = cubetypevbsp.replace("\t","").replace("vartochange(id)",f"<{itemsdict[itemkey][0].upper()}>")

            add_text(text,assetmanager.format_string(cubetypevbsp))

        def timertypeadd():
            cubetypevbsp = assetmanager.getdata("vbsp/timer")

            #Replace vars
            cubetypevbsp = cubetypevbsp.replace("\t","").replace("vartochange(id)",f"<{itemsdict[itemkey][0].upper()}>")

            add_text(text,assetmanager.format_string(cubetypevbsp))

        def enabletypeadd():
            cubetypevbsp = assetmanager.getdata("vbsp/enable")

            #Replace vars
            cubetypevbsp = cubetypevbsp.replace("\t","").replace("vartochange(id)",f"<{itemsdict[itemkey][0].upper()}>")

            add_text(text,assetmanager.format_string(cubetypevbsp))

        def reversetypeadd():
            cubetypevbsp = assetmanager.getdata("vbsp/reverse")

            #Replace vars
            cubetypevbsp = cubetypevbsp.replace("\t","").replace("vartochange(id)",f"<{itemsdict[itemkey][0].upper()}>")

            add_text(text,assetmanager.format_string(cubetypevbsp))

        def coloradd():
            cubetypevbsp = assetmanager.getdata("vbsp/color")

            #Replace vars
            cubetypevbsp = cubetypevbsp.replace("\t","").replace("vartochange(id)",f"<{itemsdict[itemkey][0].upper()}>")

            add_text(text,assetmanager.format_string(cubetypevbsp))

        menubar = tk.Menu(popup)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=popup.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        text_menu = tk.Menu(menubar, tearoff=0)
        text_menu.add_command(label="Cube Type", command=cubetypeadd)
        text_menu.add_command(label="Button Type", command=btntypeadd)
        text_menu.add_command(label="Timer Type", command=timertypeadd)
        text_menu.add_command(label="Enable Type", command=enabletypeadd)
        text_menu.add_command(label="Reverse Type", command=reversetypeadd)
        text_menu.add_command(label="Colorizer", command=coloradd)
        text_menu.add_separator()
        text_menu.add_command(label="Add Instance Path", command=makeinstancepath)
        menubar.add_cascade(label="Text", menu=text_menu)
        popup.config(menu=menubar)
        open_file()



    vbspbutton = tk.Button(root, text="vbsp_editor",font=("Arial", 11) ,bd=0,bg=theme3,fg=theme4,command=vbsp_editor)
    vbspbutton.place(width=128, height=32,x=410, y=200)



    #Debug item (todo: check vbsp for errors and editoritems errors.)

    def debuger():

        log.loginfo("debugging")
        itemkey = finditemkey()
        print(itemkey)
        checklistfile = [f"/items/{itemsdict[itemkey][2]}/editoritems.txt",f"/items/{itemsdict[itemkey][2]}/properties.txt"]
        if os.path.isfile(f"/items/{itemsdict[itemkey][2]}/vbsp_config.cfg"):
            checklistfile.append(f"/items/{itemsdict[itemkey][2]}/vbsp_config.cfg")

        def checkforsyntax(filename,syntax1,syntax2):
            with open(filename, "r") as file:
                opening_brackets = 0
                closing_brackets = 0
                for line in file:
                    for char in line:
                        if char == syntax1:
                            opening_brackets += 1
                        elif char == syntax2:
                            closing_brackets += 1
                if opening_brackets == closing_brackets:
                    return True
                else:
                    return False

        syntaxcheck1 = ["(","{"]
        syntaxcheck2 = [")","}"]
        failed = {}
        for checkthis in checklistfile:
            for x in range(len(syntaxcheck1)):
                if checkforsyntax(packagemanager.packagesdir + checkthis,syntaxcheck1[x],syntaxcheck2[x]) == True:
                    log.loginfo(f"{os.path.basename(checkthis)} PASS: CHECK{x + 1}")
                else:
                    log.loginfo(f"{os.path.basename(checkthis)} FAIL: CHECK{x + 1}")
                    failed[itemsdict[itemkey][1]] = "Syntax Check"

            #Path checking
            if os.path.isfile(os.path.join(packagemanager.packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")) == True:
                instances = []
                with open(os.path.join(packagemanager.packagesdir,"items",itemsdict[itemkey][2],"vbsp_config.cfg")) as file:
                    editoritemslines = file.read().replace("\t","").split("\n")
                for x in editoritemslines:
                    if '"ADDOVERLAY"' in x.upper() and "INSTANCES" in x.upper():
                        instances.append(os.path.join(packagemanager.packagesdir,"resources",x.replace('"AddOverlay"','').replace('bee2/',"").replace(' ',"").replace('"',"").replace('}',"")))
                    if '"CHANGEINSTANCE"' in x.upper() and "INSTANCES" in x.upper():
                        instances.append(os.path.join(packagemanager.packagesdir,"resources",x.replace('"Changeinstance"','').replace('bee2/',"").replace(' ',"").replace('"',"").replace('}',"")))
                instances = list(set(instances))
                for instance in instances:
                    if os.path.isfile(instance):
                        log.loginfo(f"{os.path.basename(instance)} passed isfile check!")
                    else:
                        log.loginfo(f"{os.path.basename(instance)} failed isfile check!")
                        failed[itemsdict[itemkey][1]] = "Path Check"
        
        if failed:
            messagebox.showwarning("Error",f"{itemsdict[itemkey][1]} failed the checks\nThis may cause the package to cause a error!\n\nFailed Results: {failed}")
        else:
            messagebox.showinfo("Info",f"Debugger found no issues with {itemsdict[itemkey][1]}.")

    debugbutton = tk.Button(root, text="debugger",font=("Arial", 11) ,bd=0,bg=theme3,fg=theme1,command=debuger)
    debugbutton.place(width=128, height=32,x=410, y=250)

    def rmitem():
        global selected
        itemkey = finditemkey()
        if messagebox.askyesno("Remove Item",f"Are you sure you want to remove {itemsdict[itemkey][1]}?"):
            #Add some code to remove info block
            with open(os.path.join(packagemanager.packagesdir,"info.txt"),"r") as file:
                filecontent = file.read()
                rmitemlist = assetmanager.find_blocks(filecontent, '"Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')

            for item in rmitemlist:
                if f'"ID""{itemsdict[itemkey][0]}"' in item.replace("\t","").replace(" ",""):
                    log.loginfo("Found Target")
                    with open(os.path.join(packagemanager.packagesdir,"info.txt"),"w") as file:
                        print(item)
                        newfile = filecontent.replace("\t","").replace(item,"")

                        file.write(assetmanager.format_string(newfile))

            log.loginfo("Removed item info from info.txt")
            #Remove folders
            dirs = (os.path.join(packagemanager.packagesdir,"items",itemsdict[itemkey][2]),os.path.join(packagemanager.packagesdir,"resources","instances","beepkg",itemsdict[itemkey][2]))
            files = (os.path.join(packagemanager.packagesdir,"resources","materials","models","props_map_editor","palette","beepkg",f"{itemsdict[itemkey][0]}.vtf"),os.path.join(packagemanager.packagesdir,"resources","materials","models","props_map_editor","palette","beepkg",f"{itemsdict[itemkey][0]}.vmt"),os.path.join(packagemanager.packagesdir,"resources","BEE2","items","beepkg",f"{itemsdict[itemkey][0]}.png"))

            for dir in dirs:
                try:
                    forcedelete(dir)
                    log.logerror(f"Removed {dir}")
                except PermissionError:
                    log.logerror(f"No permission to remove {dir}")
                    messagebox.showerror("Error",f"No permission to remove {dir}")

            for file in files:
                try:
                    os.remove(file)
                    log.logerror(f"Removed {dir}")
                except PermissionError:
                    log.logerror(f"No permission to remove {dir}")
                    messagebox.showerror("Error",f"No permission to remove {file}")
                except FileNotFoundError:
                    pass

            #Remove from listbox
            items.remove(selected)
            listbox.delete(0, tk.END)
            for item in items:
                listbox.insert(tk.END, " " + item)

            #Select new item
            selected = choice(items)
            updatainfo()
            messagebox.showinfo("Info",f"Removed {itemsdict[itemkey][2]}.")
            log.logerror(f"Removed {itemsdict[itemkey][2]}")


    rmbutton = tk.Button(root, text="Remove Item",font=("Arial", 11) ,bd=0,bg=theme3,fg=theme4,command=rmitem)
    rmbutton.place(width=128, height=32,x=410, y=300)

    def disitem():
        global itemsdict
        itemkey = finditemkey()
        #Add some code to remove info block
        with open(os.path.join(packagemanager.packagesdir,"info.txt"),"r") as file:
            filecontent = file.read()
            rmitemlist = assetmanager.find_blocks(filecontent, '"Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')
        found = False
        for item in rmitemlist:
            if f'"ID""{itemsdict[itemkey][0]}"' in item.replace("\t","").replace(" ",""):
                log.loginfo("Found Target")
                found = True
                with open(os.path.join(packagemanager.packagesdir,"info.txt"),"w") as file:
                    newfile = filecontent.replace("\t","").replace(item,item.replace('"Item"','"DIS_Item"'))
                    file.write(assetmanager.format_string(newfile))
                log.loginfo(f"Disabled {itemsdict[itemkey][1]}")
                #Change itemdict
                itemsdict[itemkey] = [itemsdict[itemkey][0],itemsdict[itemkey][1],itemsdict[itemkey][2],True]
                updatainfo()
                messagebox.showinfo("Info",f"Disabled {itemsdict[itemkey][1]}")
        
        #Enable
        if not found:
            #Add some code to remove info block
            with open(os.path.join(packagemanager.packagesdir,"info.txt"),"r") as file:
                filecontent = file.read()
                rmitemlist = assetmanager.find_blocks(filecontent, '"DIS_Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')
            found = False
            for item in rmitemlist:
                if f'"ID""{itemsdict[itemkey][0]}"' in item.replace("\t","").replace(" ",""):
                    log.loginfo("Found Target")
                    found = True
                    with open(os.path.join(packagemanager.packagesdir,"info.txt"),"w") as file:
                        newfile = filecontent.replace("\t","").replace(item,item.replace('"DIS_Item"','"Item"'))
                        file.write(assetmanager.format_string(newfile))
                    log.loginfo(f"Enabled {itemsdict[itemkey][1]}")
                    #Change itemdict
                    itemsdict[itemkey] = [itemsdict[itemkey][0],itemsdict[itemkey][1],itemsdict[itemkey][2],False]
                    updatainfo()
                    messagebox.showinfo("Info",f"Enabled {itemsdict[itemkey][1]}")

    disablebutton = tk.Button(root, text="Toggle Item",font=("Arial", 11) ,bd=0,bg=theme3,fg=theme4,command=disitem)
    disablebutton.place(width=128, height=32,x=610, y=300)

    

    def export():
        log.loginfo("Exporting")
        shutil.make_archive(os.path.basename(filepath),"zip",packagemanager.packagesdir)
        try:
            os.makedirs(os.path.join(path,"output"))
        except FileExistsError:
            pass
        counter = 1
        if not os.path.isfile(os.path.join(path,"output",f"{os.path.basename(filepath)}.bee_pack")):
            os.rename(f"{os.path.basename(filepath)}.zip",os.path.join(path,"output",f"{os.path.basename(filepath)}"))
            messagebox.showinfo("Exported!",f'Package name:{itemsdict["info"][3]} is done exporting!\nYou can find it at {os.path.join(path,"output",f"{os.path.basename(filepath)}.bee_pack")}')
        else:
            while True:
                if not os.path.isfile(os.path.join(path,"output",f"{os.path.basename(filepath)} ({counter}).bee_pack")):
                    os.rename(f"{os.path.basename(filepath)}.zip",os.path.join(path,"output",f"{os.path.basename(filepath)} ({counter})"))
                    messagebox.showinfo("Exported!",f'Package name:{itemsdict["info"][3]} is done exporting!\nYou can find it at {os.path.join(path,"output",f"{os.path.basename(filepath)} ({counter}).bee_pack")}')
                    break
                else:
                    counter += 1
        log.loginfo("Exported!")
        log.loginfo(packagemanager.packagesdir)
        log.loginfo(os.path.basename(filepath))

    buttone = tk.Button(root, text="                    Export                    ",font=("Arial", 11) ,bd=0 ,command=export,bg=theme3,fg=theme4)
    buttone.place(x=450, y=400)

    #Handle closing

    def ending():
        if messagebox.askyesno("Warning", 'Are you sure you want to exit?\nWe dont support save and loading.\nTIP: You can export to "save" your work.'):
            forcedelete(os.path.join(path,"packages"))
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", ending)

    root.mainloop()

if __name__ == "__main__":
    intui()
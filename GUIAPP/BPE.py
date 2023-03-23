import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import zipfile
import assetmanager
import log
from random import choice
import traceback
import requests
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
        leter = "ABCDEFGHIJKLMNOPQRSTUVWXZY"
        for x in leter:
            if os.path.isdir(f"{x}:\Program Files (x86)\Steam\steamapps\common\Portal 2") == True:
                return f"{x}:\Program Files (x86)\Steam\steamapps\common\Portal 2"
            if os.path.isdir(f"{x}:\SteamLibrary\steamapps\common\Portal 2") == True:
                return f"{x}:\Program Files (x86)\Steam\steamapps\common\Portal 2"
        #Checks for p2's directory

    def on_select(event):
        global selected
        # Get the selected item from the listbox
        selected = listbox.get(listbox.curselection())[1:]
        if len(selected) <= 17:
            name_variable.set(selected)
        else:
            name_variable.set(selected[:17] + "...")
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
    theme1 = "#878787"
    theme2 = "#232323"
    theme3 = "#4d4d4d"
    items = []
    editor = []
    id = []
    global itemsdict
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
    global vbspbutton
    global listbox
    global holebutton
    global autobutton
    global menu_button
    global menu_icon
    global debugbutton
    global frame
    global buttone
    global name_box
    global button
    typevar = "Add Button Type"
    typenum = 1
    global selected
    global root
    global fuckyouforspammingbutton
    selected = None
    fuckyouforspammingbutton = 0
    root = tk.Tk()
    root.geometry("800x600+300+200")
    root.configure(bg=theme2)
    root.title("Beemod Package Editor (BPE) V.2")
    root.wm_iconbitmap(os.path.join(path,"imgs/","bpe.ico"))

    #Style stuff
    style = ttk.Style()
    style.configure("Rounded.TButton", relief="flat", background="white", 
                    padding=3, borderwidth=2, font=("Arial", 12), 
                    width=20, height=5, highlightthickness=0,
                    borderradius=5)

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
    scrollbar.config(bg='#232323')
    scrollbar.grid(column=1, row=0, sticky="ns")
    # Bind the listbox to the on_select function
    listbox.bind("<<ListboxSelect>>", on_select)

    #Information board
    name_variable = tk.StringVar()
    name_box = tk.Label(root, textvariable=name_variable,bg=theme2,fg=theme1, anchor="center",width=17,bd=0,font=("Arial", 20, "bold"))
    name_box.place(x=410, y=50)
    #Name of item

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
        log.loginfo("Package Reloaded!")

    #Autopack 
    def autopack():
        log.loginfo("Running Autopack")
        global selected
        global itemsdict
        global fuckyouforspammingbutton
        if not selected:
            fuckyouforspammingbutton += 1
            if fuckyouforspammingbutton == 5:
                messagebox.showerror("Error","You can select the items on the left list you know?")
            elif fuckyouforspammingbutton == 10:
                messagebox.showerror("Error","SELECT AN ITEM BEFORE ENTERING AUTOPACK!")
            elif fuckyouforspammingbutton == 15:
                selected = choice(items)
                name_variable.set(selected)
                messagebox.showerror("Error",f"Fine, Il choose one for you. It will be {selected}")

            else:
                messagebox.showerror("Error","Please select an item before entering Autopack!")

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
                baseassets = requests.get("https://versioncontrol.orange-gamergam.repl.co/data/baseassets")
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
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt"))))
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".vtf")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf")))}')
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
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl"))))
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".vvd")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".vvd"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd"))))
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".dx90.vtx")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".dx90.vtx")))}')
                                            shutil.copy(os.path.join(p2,f"portal2_dlc{x}",asset + ".dx90.vtx"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".dx90.vtx"))))
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".phy")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy")))}')
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
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
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
                                            log.loginfo(f'Moving asset from: {os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")} to {os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")))}')
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


    def changetheme():
        global theme1
        global root
        global menu
        global vbspbutton
        global holebutton
        global autobutton
        global debugbutton
        global menu_button
        global menu_icon
        global frame
        global popup
        global text
        global name_box
        global listbox
        global buttone
        global theme2
        global theme3
        if theme1 == "#878787":
            log.loginfo("Changing to light mode")
            theme1 = "#474747"
            theme2 = "#dedede"
            theme3 = "#7a7a7a"
            menu_icon = ImageTk.PhotoImage(use_image("menul.png",(20,20)))
        else:
            log.loginfo("Changing to dark mode")
            theme1 = "#878787"
            theme2 = "#232323"
            theme3 = "#4d4d4d"
            menu_icon = ImageTk.PhotoImage(use_image("menu.png",(20,20)))
        buttons = [vbspbutton,holebutton,autobutton,debugbutton,buttone]
        for button in buttons:
            button.configure(bg=theme3,fg=theme1)
        name_box.configure(bg=theme2,fg=theme1)
        listbox.configure(bg=theme2,fg=theme1)
        menu.configure(bg=theme2,fg=theme1)
        menu.configure(activebackground=theme1, activeforeground=theme2)
        menu_button.configure(image=menu_icon)
        frame.configure(bg=theme2)
        root.configure(bg=theme2)
        popup.configure(bg=theme2)
        popup.update_idletasks()
        root.update_idletasks()

    #Utils
    menu_icon = ImageTk.PhotoImage(use_image("menu.png",(20,20)))
    menu_button = tk.Button(root, image=menu_icon, width=16, height=16, bd=0)
    menu_button.place(x=770, y=10)
    menu = tk.Menu(root, tearoff=0, bg=theme2,fg=theme1,bd=0)
    menu.add_command(label="Reload Packages", command=refreshpack(), activebackground=theme1, activeforeground=theme2)
    menu.add_command(label="Change Package", command=changepack,activebackground=theme1, activeforeground=theme2)
    menu.add_separator()
    menu.add_command(label="Change Theme", command=changetheme,activebackground=theme1, activeforeground=theme2)

    def display_menu(event):
        menu.post(event.x_root, event.y_root)
    menu_button.bind("<Button-1>", display_menu)


    #Buttons
    autobutton = tk.Button(root, text="Autopacker",command=autopack,font=("Arial", 11) ,bd=0,bg=theme3,fg=theme1)
    autobutton.place(x=610, y=200)

    #Leak checker

    def holemaker():
        log.loginfo("Running HoleMaker")
        if not selected:
            messagebox.showerror("Error","Please select an item first!")
            return 
        itemkey = finditemkey()

        #Read editoritems.txt and find "embeddedvoxels"
        with open(os.path.join(packagemanager.packagesdir,"items",itemsdict[itemkey][2],"editoritems.txt")) as file:
            print(file.read().replace("\t",""))
            voxels = assetmanager.find_block(file.read().replace("\t",""),'"EmbeddedVoxels"')
        
        #Making a new window to allow for editing embedded voxels
        embedwin = Toplevel(root)
        embedwin.geometry("512x512")
        embedwin.title("Embed Voxels Editor")
        embedwin.configure(bg=theme2)
        name = tk.StringVar()
        namevart = itemsdict[itemkey][1]
        if len(namevart) <= 17:
            name.set(namevart)
        else:
            name.set(namevart[:17] + "...")
        ItemName = tk.Label(embedwin, textvariable=name,bg=theme2,fg=theme1, anchor="center",width=17,bd=0,font=("Arial", 20, "bold"))
        ItemName.place(x=125,y=10)

        #Do math and check pos
        #Remove unnessacary info 
        while '"Voxel"' in voxels:
            voxels.remove('"Voxel"')
        while '{' in voxels:
            voxels.remove('{')
        while '}' in voxels:
            voxels.remove('}')

        print(voxels)

        for x in range(len(voxels)):
            xt = voxels[x].replace("\t","")
            if '"Pos"' in xt:
                voxels[x] = tuple(map(int, xt[5:].replace('"','').split()))
            if '"Volume"' in xt:
                messagebox.showerror('Error!','"Volume" is not supported!')
                return
        print(voxels[1:])

        button_dict =   {
                            'Button 1': {'text': 'Button 1', 'x': 10, 'y': 10},
                            'Button 2': {'text': 'Button 2', 'x': 110, 'y': 10},
                            'Button 3': {'text': 'Button 3', 'x': 210, 'y': 10},
                        }

        #Place buttons
        for btn_text, btn_params in button_dict.items():
            button = tk.Button(embedwin, text=btn_params['text'], command=lambda: print(f'{btn_params["text"]} clicked'))
            button.place(x=btn_params['x'], y=btn_params['y'])


    holebutton = tk.Button(root, text="Hole Editor",command=holemaker,font=("Arial", 11) ,bd=0,bg=theme3,fg=theme1)
    holebutton.place(x=609, y=250)

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
            file_path = pathtovbsp
            #Format it!
            assetmanager.format_file(file_path)
            with open(file_path, "r") as file:
                text.delete("1.0", tk.END)
                text.insert("1.0", file.read())

        def add_text(text_widget, text):
            current_index = text_widget.index(tk.INSERT)
            text_widget.insert(current_index, text)

        def save_file():
            file_path = pathtovbsp
            assetmanager.format_file(file_path)
            if file_path is None:
                return
            data = text.get('1.0', 'end')
            with open(file_path, 'w') as file:
                file.write(data)
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
                file = filedialog.askopenfilename()
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

        menubar = tk.Menu(popup)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save", command=save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=popup.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        text_menu = tk.Menu(menubar, tearoff=0)
        text_menu.add_command(label="Cube Type", command=cubetypeadd)
        text_menu.add_command(label="Button Type", command=btntypeadd)
        text_menu.add_command(label="Timer Type", command=save_file)
        text_menu.add_command(label="Timer Type", command=save_file)
        text_menu.add_separator()
        text_menu.add_command(label="Add Instance Path", command=makeinstancepath)
        menubar.add_cascade(label="Text", menu=text_menu)
        popup.config(menu=menubar)
        open_file()



    vbspbutton = tk.Button(root, text="vbsp_editor",font=("Arial", 11) ,bd=0,bg=theme3,fg=theme1,command=vbsp_editor)
    vbspbutton.place(x=410, y=200)



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

        syntaxcheck1 = ["(",r"{","'"]
        syntaxcheck2 = [")",r"}","'"]
        failed = []
        for checkthis in checklistfile:
            for x in range(len(syntaxcheck1)):
                if checkforsyntax(packagemanager.packagesdir + checkthis,syntaxcheck1[x],syntaxcheck2[x]) == True:
                    log.loginfo(f"{os.path.basename(checkthis)} PASS: CHECK{x + 1}")
                else:
                    log.loginfo(f"{os.path.basename(checkthis)} FAIL: CHECK{x + 1}")
                    failed.append(os.path.basename(checkthis))

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
                        failed.append(os.path.basename(instance))
        
        if failed:
            messagebox.showerror("Error",f"{itemsdict[itemkey][1]} failed the checks")



        

    debugbutton = tk.Button(root, text="debugger",font=("Arial", 11) ,bd=0,bg=theme3,fg=theme1,command=debuger)
    debugbutton.place(x=415, y=250)

    def export():
        log.loginfo("Exporting")
        try:
            os.remove(os.path.basename(filepath))
        except:
            pass
        shutil.make_archive(os.path.basename(filepath), 'zip', packagemanager.packagesdir)
        shutil.copy(os.path.basename(filepath) + ".zip",os.path.basename(filepath))
        os.remove(os.path.basename(filepath) + ".zip")
        messagebox.showinfo("Exported!",f'Package name:{itemsdict["info"][3]} is done exporting!\nYou can find it at {path}')
        log.loginfo("Exported!")
        log.loginfo(packagemanager.packagesdir)
        log.loginfo(os.path.basename(filepath))

    buttone = tk.Button(root, text="                    Export                    ",font=("Arial", 11) ,bd=0 ,command=export,bg=theme3,fg=theme1)
    buttone.place(x=450, y=400)

    root.mainloop()

if __name__ == "__main__":
    intui()
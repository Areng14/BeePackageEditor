import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import zipfile
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

    if os.path.basename(sys.executable) == "python.exe":
        path = __file__.replace(os.path.basename(__file__),"")
    else:
        path = sys.executable.replace(os.path.basename(sys.executable),"")

    imgdir = os.path.join(path,"imgs/")

    def use_image(name_img,wxh):
        img = Image.open(os.path.join(imgdir,name_img))
        return img.resize(wxh)

    items = []
    editor = []
    id = []
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
    typevar = "Add Button Type"
    typenum = 1
    root = tk.Tk()
    root.geometry("800x600+300+200")
    root.configure(bg="#232323")
    root.title("Beemod Package Editor (BPE) V.2")

    #Style stuff
    style = ttk.Style()
    style.configure("Rounded.TButton", relief="flat", background="white", 
                    padding=3, borderwidth=2, font=("Arial", 12), 
                    width=20, height=5, highlightthickness=0,
                    borderradius=5)

    # Create a list of items

    # Create a tk.Frame to hold the listbox
    frame = tk.Frame(root, bg="#232323",padx=10,pady=10)
    frame.grid(column=0, row=0)

    # Create a tk.Listbox
    listbox = tk.Listbox(frame, height=36, width=50, bg="#232323",fg="#878787", bd=0, highlightthickness=0)
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
    name_box = tk.Label(root, textvariable=name_variable,bg="#232323",fg="#878787", anchor="center",width=17,bd=0,font=("Arial", 20, "bold"))
    name_box.place(x=410, y=50)
    #Name of item

    #Refresh Package
    def refreshpack():
        items.clear()
        editor.clear()
        id.clear()
        with open(os.path.join(path,"config.bpe"),"r") as config:
            itemsdict = packagemanager.readfile(config.read())
        for x in range(len(itemsdict) - 1):
            appendthis = itemsdict[x]
            items.append(appendthis[1])
            editor.append(appendthis[2])
            id.append(appendthis[0])
        listbox.delete(0, tk.END)
        for item in items:
            listbox.insert(tk.END, " " + item)
        print("Package Reloaded!")

    #Autopack 
    def autopack():
        global selected
        if not selected:
            messagebox.ERROR("Please select an item before entering Autopack!")
        else:
            itemcall = selected[1:]
            #Find key for selected
            for x in itemsdict:
                if itemcall in itemsdict[x][1]:
                    itemkey = x 
                    break
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
            
            #Getting the list from an "api" because its too long
            baseassets = requests.get("https://versioncontrol.orange-gamergam.repl.co/data/baseassets")
            baseassets = baseassets.text.replace(" ","").replace("'","").split(",")
            for x in range(len(packlist)):
                if os.path.splitext(os.path.basename(packlist[x]))[0].upper() in baseassets:
                    packlist[x] = "PACKER_IGNORE"

            #Packing!
            p2 = findp2dir()
            errors = []
            for asset in packlist:
                if asset != "PACKER_IGNORE":
                    if asset[:8] == "material":
                        #Material packing!
                        #Making folders
                        packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + ".vtf").replace(os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf")),""))
                        if os.path.isdir(packagematpath) == False:
                            os.makedirs(packagematpath.lower())
                        #Finding the .vtf and the .vmt
                        counter = 0
                        for x in range(999):
                            if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt")) == True:
                                try:
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + ".vmt"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vmt"))))
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + ".vtf"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtf"))))
                                    break
                                except:
                                    counter += 1000
                            counter += 1
                        if counter >= 999:
                            errors.append(asset.lower())
                    if asset[:6] == "models":
                        #Model packing!
                        #Making folders
                        packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + ".mdl").replace(os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl")),""))
                        if os.path.isdir(packagematpath) == False:
                            os.makedirs(packagematpath.lower())
                        #Finding the .vtf and the .vmt
                        counter = 0
                        for x in range(999):
                            if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl")) == True:
                                try:
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + ".mdl"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".mdl"))))
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + ".vvd"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vvd"))))
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + ".vtx"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".vtx"))))
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + ".phy"), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + ".phy"))))
                                    break
                                except:
                                    counter += 1000 
                            counter += 1
                        if counter >= 999:
                            errors.append(asset.lower())
                    if asset[:6] == "scripts":
                        #Sound packing!
                        #Making folders
                        extension = ".nut"
                        packagematpath = os.path.join(os.path.join(packagesdir,"resources",asset + extension).replace(os.path.basename(os.path.join(packagesdir,"resources",asset + extension)),""))
                        if os.path.isdir(packagematpath) == False:
                            os.makedirs(packagematpath.lower())
                        #Finding the .vtf and the .vmt
                        counter = 0
                        for x in range(999):
                            if os.path.isfile(os.path.join(p2,f"portal2_dlc{x}",asset + extension)) == True:
                                try:
                                    os.rename(os.path.join(p2,f"portal2_dlc{x}",asset + extension), os.path.join(packagematpath.lower(),os.path.basename(os.path.join(packagesdir,"resources",asset + extension))))
                                    break
                                except:
                                    counter += 1000 
                            counter += 1
                        if counter >= 999:
                            errors.append(asset.lower())
            if errors:
                messagebox.showwarning("Warning!","----------------------------------------\n" + '\n'.join(str(i) for i in errors) + "\n----------------------------------------\n\nWe could not find the assets in your portal 2 dlc folders.\nThese may be base BEE and P2 assets.")
            else:
                messagebox.showinfo("Info",f"Assets sucessfully packed for {selected}")


    #Change package
    def changepack():
        filepath = filedialog.askopenfilename()
        if messagebox.askyesnocancel("Error", f"Do you want to open {os.path.basename(filepath)}?") == True:
            try:
                shutil.rmtree(os.path.join(path,"packages"),ignore_errors = True)
                os.makedirs(os.path.join(path,"packages"))
                with zipfile.ZipFile( filepath, 'r') as zip_ref:
                    txtfile = zip_ref.open('info.txt', 'r')
                    txtlist = txtfile.read().decode().split("\n")
                if "//" in txtlist[0]:
                    with open(os.path.join(path,"config.bpe"),"w") as config:
                        config.write(filepath)
                    refreshpack()
                else:
                    result = messagebox.askyesno("Error", "Not a BeePKG package!\nWould you like to open this anyways?\nYou may encounter errors by doing this.")
                    if result == True:
                        with open(os.path.join(path,"config.bpe"),"w") as config:
                            config.write(filepath)
                        refreshpack()
            except Exception as error:
                pyperclip.copy(traceback.format_exc())
                messagebox.showerror("Error", traceback.format_exc(), detail= "This has been copied to the clipboard.")

    #Utils
    menu_icon = ImageTk.PhotoImage(use_image("menu.png",(20,20)))
    menu_button = tk.Button(root, image=menu_icon, width=16, height=16, bd=0)
    menu_button.place(x=770, y=10)
    menu = tk.Menu(root, tearoff=0, bg="#232323",fg="#878787",bd=0)
    menu.add_command(label="Reload Packages", command=refreshpack(), activebackground="#878787", activeforeground="#232323")
    menu.add_command(label="Change Package", command=changepack,activebackground="#878787", activeforeground="#232323")
    def display_menu(event):
        menu.post(event.x_root, event.y_root)
    menu_button.bind("<Button-1>", display_menu)


    #Buttons
    button = tk.Button(root, text="Autopacker",command=autopack,font=("Arial", 11) ,bd=0,bg="#4d4d4d",fg="#878787")
    button.place(x=610, y=200)


    #Buttons (Add Types)

    def changetype(event):
        global  typenum
        print("Changing text!")
        if typenum == 1:
            typenum += 1
            button.config(text="Add Button Type")
        elif typenum == 2:
            typenum += 1
            button.config(text="Add Cube Type")
        elif typenum == 3:
            typenum += 1
            button.config(text="Add Timer Type")
        elif typenum == 4:
            typenum += 1
            button.config(text="Add Start Enabled")
        elif typenum == 5:
            typenum = 1
            button.config(text="Add Start Reversed")


    def types(event):
        global typenum
        top = Toplevel(root)
        top.configure(bg="#232323")
        top.geometry("256x384")
        top.title("Add Types")
        if typenum == 2:
            pass
        elif typenum == 3:
            print("cube type")
        elif typenum == 4:
            print("timer")
        elif typenum == 5:
            print("Enabled")
        elif typenum == 1:
            print("Reversed")

    button = tk.Button(root, text=typevar,font=("Arial", 11) ,bd=0,bg="#4d4d4d",fg="#878787")
    button.bind("<Button-1>", types)
    button.bind("<Button-3>", changetype)
    button.bind("<Button-2>", changetype)
    button.place(x=410, y=200)

    def export():
        try:
            os.remove(os.path.basename(filepath))
        except:
            pass
        shutil.make_archive(os.path.basename(filepath), 'zip', packagemanager.packagesdir)
        os.rename(os.path.basename(filepath) + ".zip",os.path.basename(filepath))
        messagebox.showinfo("Exported!",f'Package name:{itemsdict["info"][3]} is done exporting!\nYou can find it at {path}')
        print("Exported!")
        print(packagemanager.packagesdir)
        print(os.path.basename(filepath))

    buttone = tk.Button(root, text="                    Export                    ",font=("Arial", 11) ,bd=0 ,command=export,bg="#4d4d4d",fg="#878787")
    buttone.place(x=450, y=400)

    root.mainloop()

if __name__ == "__main__":
    intui()
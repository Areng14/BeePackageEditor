import os
import shutil

def forcedelete(dir):
    while os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=True)

if messagebox.askyesno("Remove Item",f"Are you sure you want to remove {item[1]}?"):
    #Add some code to remove info block
    with open(os.path.join(packagemanager.packagesdir,"info.txt"),"r") as file:
        filecontent = file.read()
        rmitemlist = assetmanager.find_blocks(filecontent, '"Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*') + assetmanager.find_blocks(filecontent, '"DIS_Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')
    for fitem in rmitemlist:
        if f'"ID""{item[0]}"' in fitem.replace("\t","").replace(" ",""):
            with open(os.path.join(packagemanager.packagesdir,"info.txt"),"w") as file:
                newfile = filecontent.replace("\t","").replace(fitem,"")
                file.write(assetmanager.format_string(newfile))
    log.loginfo("Removed item info from info.txt")
    #Remove folders
    dirs = (os.path.join(packagemanager.packagesdir,"items",item[2]),os.path.join(packagemanager.packagesdir,"resources","instances","beepkg",item[2]))
    files = (os.path.join(packagemanager.packagesdir,"resources","materials","models","props_map_editor","palette","beepkg",f"{item[0]}.vtf"),os.path.join(packagemanager.packagesdir,"resources","materials","models","props_map_editor","palette","beepkg",f"{item[0]}.vmt"),os.path.join(packagemanager.packagesdir,"resources","BEE2","items","beepkg",f"{item[0]}.png"))
    for dir in dirs:
        try:
            forcedelete(dir)
            log.loginfo(f"Removed {dir}")
        except PermissionError:
            log.logerror(f"No permission to remove {dir}")
            messagebox.showerror("Error",f"No permission to remove {dir}")
    for file in files:
        file = file.replace('"',"")
        try:
            os.remove(file)
            log.loginfo(f"Removed {dir}")
        except PermissionError:
            log.logerror(f"No permission to remove {dir}")
            messagebox.showerror("Error",f"No permission to remove {file}")
        except FileNotFoundError:
            pass
    #Remove from listbox
    updateitem()
    refreshitems()
    messagebox.showinfo("Info",f"Removed.")
    log.logerror(f"Removed")
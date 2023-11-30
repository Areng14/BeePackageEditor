import os

with open(os.path.join(packagemanager.packagesdir,"info.txt"),"r") as file:
    filecontent = file.read()
    rmitemlist = assetmanager.find_blocks(filecontent, '"Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')
found = False
for fitem in rmitemlist:
    if f'"ID""{item[0]}"' in fitem.replace("\t","").replace(" ",""):
        log.loginfo("Found Target")
        found = True
        with open(os.path.join(packagemanager.packagesdir,"info.txt"),"w") as file:
            newfile = filecontent.replace("\t","").replace(fitem,fitem.replace('"Item"','"DIS_Item"'))
            file.write(assetmanager.format_string(newfile))
        log.loginfo(f"Disabled {item[1]}")
        #Change itemdict
        item = [item[0],item[1],item[2],True]
        updateitem()
        refreshitems()
        messagebox.showinfo("Info",f"Disabled {item[1]}")

#Enable
if not found:
    #Add some code to remove info block
    with open(os.path.join(packagemanager.packagesdir,"info.txt"),"r") as file:
        filecontent = file.read()
        rmitemlist = assetmanager.find_blocks(filecontent, '"DIS_Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')
    found = False
    for fitem in rmitemlist:
        if f'"ID""{item[0]}"' in fitem.replace("\t","").replace(" ",""):
            log.loginfo("Found Target")
            found = True
            with open(os.path.join(packagemanager.packagesdir,"info.txt"),"w") as file:
                newfile = filecontent.replace("\t","").replace(fitem,fitem.replace('"DIS_Item"','"Item"'))
                file.write(assetmanager.format_string(newfile))
            log.loginfo(f"Enabled {item[1]}")
            #Change itemdict
            item = [item[0],item[1],item[2],False]
            updateitem()
            refreshitems()
            messagebox.showinfo("Info",f"Enabled {item[1]}")
def forcedelete(dir):
    while os.path.isdir(dir):
        shutil.rmtree(dir, ignore_errors=True)

def remove_whitespace_except_in_quotes(text):
    """ Removes whitespace from text except within quotes. """
    def replace(match):
        return match.group(0) if match.group(0).startswith('"') else ''.join(match.group(0).split())
    return re.sub(r'(".*?"|\S+)', replace, text)

def update_info_file(info_path, new_content):
    """ Updates the info file with new content. """
    with open(info_path, "w") as file:
        file.write(new_content)

def remove_item(item):
    with open(os.path.join(packagemanager.packagesdir, "info.txt"), "r") as file:
        filecontent = file.read()
        rmitemlist = assetmanager.find_blocks(filecontent, '"Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')
        dis_item_list = assetmanager.find_blocks(filecontent, '"DIS_Item"', r'{key}\s*{{[^}}]*}}\s*}}\s*}}\s*')

        if dis_item_list:
            rmitemlist.extend(dis_item_list)


    for item_block in rmitemlist:
        if f'"ID""{item[0]}"' in item_block.replace("\t", "").replace(" ", ""):
            with open(os.path.join(packagemanager.packagesdir, "info.txt"), "w") as file:
                log.loginfo(item_block)
                newfile = filecontent.replace("\t", "").replace(item_block, "")
                file.write(assetmanager.format_string(newfile))
    log.loginfo("Removed item info from info.txt")

    # Remove folders and files
    dirs = (os.path.join(packagemanager.packagesdir, "items", item[2]), os.path.join(packagemanager.packagesdir, "resources", "instances", "beepkg", item[2]))
    files = (os.path.join(packagemanager.packagesdir, "resources", "materials", "models", "props_map_editor", "palette", "beepkg", f"{item[0]}.vtf"), os.path.join(packagemanager.packagesdir, "resources", "materials", "models", "props_map_editor", "palette", "beepkg", f"{item[0]}.vmt"), os.path.join(packagemanager.packagesdir, "resources", "BEE2", "items", "beepkg", f"{item[0]}.png"))

    for dir in dirs:
        try:
            forcedelete(dir)
            log.logerror(f"Removed {dir}")
        except PermissionError:
            log.logerror(f"No permission to remove {dir}")
            messagebox.showerror("Error", f"No permission to remove {dir}")

    for file in files:
        try:
            os.remove(file)
            log.logerror(f"Removed {file}")
        except PermissionError:
            log.logerror(f"No permission to remove {file}")
            messagebox.showerror("Error", f"No permission to remove {file}")
        except FileNotFoundError:
            pass

print(item[0])
if mselect == False:
    if messagebox.askyesno("Remove Item",f"Are you sure you want to remove {item[1]}?"):
        remove_item(item)
else:
    if itemcount == 0:
        if messagebox.askyesno("Remove Item",f"Are you sure you want to remove {', '.join([str(item[1]) for item in mselection])}?"):
            remove_item(item)
    else:
        remove_item(item)

updateitem()
refreshitems()
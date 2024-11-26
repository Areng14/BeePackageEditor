lookfor = []

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
            conf = srctools.Keyvalues.parse(file)
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

    #save to plugin save
    save_plugin_data(plugin_name,"p2dir",p2dir)
    return p2dir

#Search editoritems.txt
with open(os.path.join(packagemanager.packagesdir,"items",item[2],"editoritems.txt")) as file:
    editoritemslines = file.read().replace("\t","").split("\n")
for x in editoritemslines:
    if '"NAME"' in x.upper() and "INSTANCES" in x.upper():
        lookfor.append(x.replace('"Name"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
#Search vbsp_config (if it exists)
if os.path.isfile(os.path.join(packagemanager.packagesdir,"items",item[2],"vbsp_config.cfg")) == True:
    with open(os.path.join(packagemanager.packagesdir,"items",item[2],"vbsp_config.cfg")) as file:
        editoritemslines = file.read().replace("\t","").split("\n")
    for x in editoritemslines:
        if '"ADDOVERLAY"' in x.upper() and "INSTANCES" in x.upper():
            lookfor.append(x.replace('"AddOverlay"','').replace('BEE2/',"").replace(' ',"").replace('"',""))
        if '"CHANGEINSTANCE"' in x.upper() and "INSTANCES" in x.upper():
            lookfor.append(x.replace('"ChangeInstance"','').replace('BEE2/',"").replace(' ',"").replace('"',""))

#Once we have gotten the instances we want to check if it actually exists or not
instancelist = []
for x in list(set(lookfor)):
    if os.path.isfile(os.path.join(packagemanager.packagesdir,"resources",x)) == True:
        instancelist.append(x)
packlist = []
for instance in instancelist:
    packdict = packagemanager.readvmf(os.path.join(packagemanager.packagesdir,"resources",instance),"MODEL,MATERIAL,SOUND,SCRIPT")
    for key, value in packdict.items():
        if value:
            for sublist in value:
                packlist.append(sublist.lower())

#Find the dependent materials for models
if not get_plugin_data(plugin_name,"p2dir"):
    log.loginfo("Couldnt find p2dir in config finding p2dir...")
    p2 = findp2dir()
else:
    log.loginfo("Found p2dir from config.")
    p2 = get_plugin_data(plugin_name,"p2dir")
dependentassets = []
packlist = list(set(packlist))
for assets in packlist:
    if assets[:6] == "models":
        for deassets in assetmanager.finedepen(assets,p2):
            dependentassets.append(deassets)
#combine the 2 lists
packlist.extend(dependentassets)
#Remove duplicate
packlist = list(set(packlist))

baseassets = requests.get("https://versioncontrol-areng123.replit.app/data/baseassets")
baseassets = baseassets.text.replace(" ","").replace("'","").split(",")
for x in range(len(packlist)):
    if os.path.splitext(os.path.basename(packlist[x]))[0].upper() in baseassets:
        packlist[x] = "PACKER_IGNORE"
log.loginfo(f"Packages that needs to be packed: {packlist}")

#Changing to be a c: file
with open(os.path.join(p2,"portal2","gameinfo.txt"), 'r') as file:
    gameinfo_content = file.read()

# Define the regex pattern
pattern = r'Game\s+("[^"]+"|\w+)'

# Find all matches
searchdirs = re.findall(pattern, gameinfo_content)

#Find portal2_dirx folders
count = 1
while True:
    if not os.path.isfile(os.path.join(p2,f"portal2_dlc{count}")):
        break
    else:
        searchdirs.append(f"portal2_dlc{count}")

cpath = []

for dir in searchdirs:
    dir = dir.replace('"',"")
    for path in packlist:
        if path != "PACKER_IGNORE":
            if path[:8] == "material":
                if os.path.isfile(os.path.join(p2,dir,f"{path}.vtf")):
                    cpath.append(os.path.join(p2,dir,f"{path}.vtf"))
                    cpath.append(os.path.join(p2,dir,f"{path}.vmt"))
            elif path[:6] == "models":
                path = path.replace(".mdl","")
                if os.path.isfile(os.path.join(p2,dir,f"{path}.mdl")):
                    cpath.append(os.path.join(p2,dir,f"{path}.mdl"))
                    cpath.append(os.path.join(p2,dir,f"{path}.phy"))
                    cpath.append(os.path.join(p2,dir,f"{path}.vvd"))
                    cpath.append(os.path.join(p2,dir,f"{path}.dx90.vtx"))
            elif path[:6] == "message":
                extension = os.path.splitext(os.path.basename(path))[1]
                cpath.append(os.path.join(p2,dir,f"{path}{extension}"))
            elif path[:6] == "scripts":
                cpath.append(os.path.join(p2,dir,f"{path}.nut"))
            else:
                log.logerror(f"Couldnt find {os.path.basename(path)}")

for asset in cpath:
    #Now we pack it to the packages thing.
    dirlen = len(p2.replace("\\","/").split("/"))

    isoasset = '\\'.join(asset.replace("\\","/").split("/")[dirlen + 1:])

    #Pack
    #Check if it exists
    if os.path.isfile(os.path.join(packagemanager.packagesdir,"resources",isoasset)):
        log.loginfo(f"{os.path.splitext(os.path.basename(asset))[0]} is already packed!")
    else:
        try:
            os.makedirs(os.path.join(packagemanager.packagesdir,"resources",isoasset).replace(os.path.basename(asset),""))
        except FileExistsError:
            pass
        shutil.copy(asset,os.path.join(packagemanager.packagesdir,"resources",isoasset))
        log.loginfo(f"Packed: {os.path.splitext(os.path.basename(asset))[0]}")

#Verify
log.loginfo(f"Verifying packs")
packcount = 0
npacklist = []

for asset2 in cpath:
    isoasset = '\\'.join(asset2.replace("\\","/").split("/")[dirlen + 1:])
    if os.path.isfile(os.path.join(packagemanager.packagesdir,"resources",isoasset)):
        packcount += 1
        npacklist.append(os.path.basename(os.path.join(packagemanager.packagesdir,"resources",isoasset)))

if packcount == len(cpath):
    if npacklist:
        if len(npacklist) > 20:
            pklist = '\n'.join(npacklist[:20]) + "\n..."
        else:
            pklist = '\n'.join(npacklist)
    else:
        pklist = F"None. All items were default items"

    messagebox.showinfo("Info", f"Packed assets for {item[1]}\nList of packed items\n\n{pklist}")
    log.loginfo("Verified.")
else:
    messagebox.showwarning("Warning", f"Not everything was packed!\n\nThis may be due to you not having the assets\nOr autopack is missing permissions.")
    log.loginfo("Failed.")
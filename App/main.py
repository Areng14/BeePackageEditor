import zipfile
import os
import shutil
import sys
import requests
import keyboard
from webbrowser import open as webopen
from colorama import Fore, Style, init
from math import ceil
import time

version = "1.2_DEV"


def findp2dir():
    leter = "ABCDEFGHIJKLMNOPQRSTUVWXZY"
    for x in leter:
        if os.path.isdir(f"{x}:\Program Files (x86)\Steam\steamapps\common\Portal 2") == True:
            return f"{x}:\Program Files (x86)\Steam\steamapps\common\Portal 2"
        if os.path.isdir(f"{x}:\SteamLibrary\steamapps\common\Portal 2") == True:
            return f"{x}:\Program Files (x86)\Steam\steamapps\common\Portal 2"
    #Checks for p2's directory

def findmaxdlc():
    pointer = 1
    while True:
        if os.path.isdir(os.path.join(findp2dir(),f"portal2_dlc{pointer}")) == False:
            return pointer
        pointer += 1
        

def menu(options,cursorop="[ ",selectcolor=Fore.GREEN):
    init(convert=True)
    pagenum = 1
    def option(intv):
        nonlocal cursorop
        #You may choose the "cursor" letter
        nonlocal options
        nonlocal pagenum
        nonlocal selectcolor
        printlist = []
        for x in range(100):
            print("\n")
        if len(options) > 10:
            for x in range((pagenum * 10) - 10,pagenum * 10,1):
                if x != intv:
                    printlist.append("RB_" + options[x])
                    
                else:
                    printlist.append("GB_" + cursorop + options[x] + "_R_")
            printthis = ""
            for x in range(len(printlist)):
                printthis = printthis  + printlist[x] + "\n"
            printthis = str(printthis).replace("RB_",Style.RESET_ALL + Style.BRIGHT).replace("GB_",Style.BRIGHT + Fore.GREEN).replace("_R_",Style.RESET_ALL).replace("'","")
            sys.stdout.write(r"----------------{Options}----------------" + f"\nPage [{pagenum}/{int(str((int(ceil(len(options) / 10.0)) * 10))[0])}]\nUse arrow keys to navigate!\nWarning! If you have epilepsy, please proceed with caution\nIf the 'Cursor' disapears press 'R' to reset it.\nPress enter to confirm.\n\n" + printthis + "\n")
            sys.stdout.flush
        else:
            for x in range(len(options)):
                if x != intv:
                    printlist.append("RB_" + options[x])
                    
                else:
                    printlist.append("GB_" + cursorop + options[x] + "_R_")
            printthis = ""
            for x in range(len(printlist)):
                printthis = printthis  + printlist[x] + "\n"
            printthis = str(printthis).replace("RB_",Style.RESET_ALL + Style.BRIGHT).replace("GB_",Style.BRIGHT + Fore.GREEN).replace("_R_",Style.RESET_ALL).replace("'","")
            sys.stdout.write(r"----------------{Options}----------------" + "\nWarning! If you have epilepsy, please proceed with caution\nIf the 'Cursor' disapears press 'R' to reset it.\nPress enter to confirm.\n\n" + printthis + "\n")
            sys.stdout.flush
        #We print out the options
    whereami = 0
    for x in range((int(ceil(len(options) / 10.0)) * 10) - len(options)):
        options.append("")
    option(whereami)
    while True:
        if keyboard.is_pressed("up arrow"):
            if whereami != 0:
                option(whereami - 1)
                whereami -= 1
                time.sleep(0.1) 
        if keyboard.is_pressed("down arrow"):
            if whereami != len(options) - 1:
                option(whereami + 1)
                whereami += 1
                time.sleep(0.1) 
        if keyboard.is_pressed("R"):
            whereami = 0
            pagenum = 1
            option(whereami)
        if len(options) > 10:
            if keyboard.is_pressed("left arrow"):
                if pagenum != 1:
                    pagenum -= 1
                    option(whereami - 10)
                    whereami -= 10
                    time.sleep(0.1)
            if keyboard.is_pressed("right arrow"):
                if pagenum != int(str((int(ceil(len(options) / 10.0)) * 10))[0]):
                    pagenum += 1
                    option(whereami + 10)
                    whereami += 10
                    time.sleep(0.1)
        if keyboard.is_pressed("Enter"):
            break
        #Button Selection
    for x in range(500):
        print("\n")
    return options[whereami]

def main():
    timev = time.time()
    def clear():
        for x in range(100):
            log("\n")

    def log(text):
        with open(os.path.join(path,f"logs/BPE_LOG[{timev}].txt"), 'a') as file:
            file.write(str(text) + "\n")
            print(f"[LOGS IGNORE!] {text}")
    if os.path.basename(sys.executable) == "python.exe":
        path = __file__.replace(os.path.basename(__file__),"")
    else:
        path = sys.executable.replace(os.path.basename(sys.executable),"")
    if os.path.isfile(os.path.join(path,"package/info.txt")) == True:
        while True:
            with open(os.path.join(path,"package/info.txt"), 'r') as file:
                if file.readline().replace(" ","")[:4] != '"ID"':
                    if file.readline().replace(" ","")[:4] != '"ID"':
                        log("Error! info.txt is not the right format!")
                        time.sleep(2)
                        shutil.rmtree(os.path.join(path,"package"))
                        if os.path.isdir(os.path.join(path,"package")) == False:
                            os.mkdir(os.path.join(path,"package"))
                        log("Deleted packages.")
                        return
                lengthvar = len(file.readlines())
            with open(os.path.join(path,"package/info.txt"), 'r') as file:
                file.readline()
                file.readline()
                info = {
                    "Name" : file.readline()[6:].replace('"',"").replace("\n",""),
                    "Desc" : file.readline()[6:].replace('"',"").replace("\n","")
                }
                items = {}
                itemnum = 1
                check = 0
                check2 = 0
                reader = []
                for x in range(lengthvar):
                    reader.append(file.readline().replace("\n",""))
                for x in range(len(reader)):
                    log(reader[x])
                    if '"Item"' == reader[x]:
                        for y in range(10):
                            readervar = reader[x + y]
                            if '"ID"' in readervar[:5]:
                                log("found a ID")
                                ID = readervar[6:].replace('"',"")
                                check = 1
                            if '"BEE2_CLEAN"' in readervar[:15]:
                                log("found a NAME")
                                Name = readervar[16:].replace('"',"")
                                check2 = 1
                            if check == 1 and check2 == 1:
                                if Name != "" and ID != "":
                                    check = 0
                                    check2 = 0
                                    items[str(itemnum) + "_ID"] = ID
                                    items[str(itemnum) + "_Name"] = Name
                                    items[str(itemnum) + "_NameS"] = Name.replace("_"," ")
                                    ID = ""
                                    Name = ""
                                    itemnum += 1
                                    break
                            readervar = ""
            log(items)
            #Finished with getting information from info.txt
            #We will rescan this later when button is finished

            #Start a menu
            while True:
                menulist = []
                for x in range(round(len(items) / 3)):
                    menulist.append(items.get(f"{x + 1}_NameS")[:1].upper() + items.get(f"{x + 1}_NameS")[1:])
                menulist.append("")
                menulist.append(r"---------{Utilities}---------")
                menulist.append("Check for updates")
                menulist.append("Exit")
                menulist.append("Pack")
                itemchoice = menu(menulist)

                #Starts listening for utility buttons
                if itemchoice == "":
                    pass
                elif itemchoice == r"---------{Utilities}---------":
                    pass
                elif itemchoice == "Check for updates":
                    dev_index = version.index("_DEV")
                    dev_string = version[dev_index:]
                    if dev_string != "_DEV":
                        if requests.get("https://versioncontrol.orange-gamergam.repl.co/api/bpe").json() == version:
                            print("No updates are currently available.")
                        else:
                            print(f'There is an update available. You are using ({version}) Newest is ({requests.get("https://versioncontrol.orange-gamergam.repl.co/api/bpe").json()})')
                            print("You can get the update here https://github.com/Areng14/BeePackageEditor/releases")
                            time.sleep(5)
                            webopen("https://github.com/Areng14/BeePackageEditor/releases")
                    else:
                        print("You are currently using the DEV versions. Therefor no updates will be here.")
                    print("Press enter to continue:")
                    while True:
                        if keyboard.is_pressed("Enter"):
                            break
                elif itemchoice == "Exit":
                    time.sleep(1)
                    shutil.rmtree(os.path.join(path,"package"))
                    if os.path.isdir(os.path.join(path,"package")) == False:
                        os.mkdir(os.path.join(path,"package"))
                    return
                elif itemchoice == "Pack":
                    ID = info["Name"].replace("'","").replace(" ","_").replace('"',"")[1:]
                    shutil.make_archive(ID, 'zip',os.path.join(path, "package"))
                    base = os.path.splitext(ID)[0]
                    os.rename(ID + ".zip", base + '.bee_pack')
                    shutil.move(path + ID + ".bee_pack",os.path.join(path, "output/" + ID + ".bee_pack"))
                    print("Operation Completed. (Press Enter)")
                else:
                    break

            #Converting item choice to int
            for x in range(round(len(items) / 3)):
                if items[f"{x + 1}_NameS"] == itemchoice.lower():
                    intvalue = x + 1
                    break
            log("intvalue = " + str(intvalue))


            #Start a menu to choose what to do

            choicechoice = menu(["Add Types","Asset Packer","Remove Item","Input Editor","Output Editor","Hole Maker","","----------------","Back"])
            #Add/Remove input
            if choicechoice == "Back":
                pass

            if choicechoice == "Add Types":
                choice = menu(["Timer Type [30]","Cube Type [5]","Button Type [3]","Start Enabled [1]","Start Reversed [1]","","----------------","Back"])
                datafile = False
                if choice == "Timer Type [30]":
                    inputinsert = '"TimerDelay"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "TimerDelay"
                    datafile = "data/Timerdata.bpe_data"
                    num = 3
                if choice == "Cube Type [5]":
                    inputinsert = '"CubeType"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "CubeType"
                    datafile = "data/Cubedata.bpe_data"
                    num = 0
                if choice == "Button Type [3]":
                    inputinsert = '"ButtonType"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "ButtonType"
                    datafile = "data/Buttondata.bpe_data"
                    num = 0
                if choice == "Start Enabled [1]":
                    inputinsert = '"StartEnabled"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "StartEnabled"
                    datafile = "data/Enabledata.bpe_data"
                    num = 1
                if choice == "Start Reversed [1]":
                    inputinsert = '"StartReversed"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "StartReversed"
                    datafile = "data/Reversedata.bpe_data"
                    num = 1
                if datafile != False:
                    with open(os.path.join(path,datafile),"r") as file:
                        listv = file.read().replace("\t","").split("\n")
                    for x in range(len(listv)):
                        if listv[x] == 'VAR(ID)':
                            listv[x] = f'"instance" "<{items[f"{intvalue}_ID"].replace(" ","")}>"'
                        if listv[x] == "VAR(PATH)":
                            listv[x] = f'"Changeinstance" "instances/bee2/beepkg/{items[f"{intvalue}_Name"]}/{items[f"{intvalue}_Name"]}_{num}.vmf"'
                            num += 1
                        log(listv[x])
                    
                    with open(os.path.join(path,f'package/items/{items[f"{intvalue}_Name"]}/vbsp_config.cfg'),"w") as file:
                        for x in range(len(listv)):
                            file.write(listv[x] + "\n")
                    #Removing old types
                        
                    filecontent = []
                    checkforused = ["StartReversed","StartEnabled","ButtonType","CubeType","TimerDelay"]
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        listvvv = file.read().replace("\t","").split("\n")
                    for x in range(len(listvvv)):
                        if listvvv[x] == '"Properties"':
                            removeline = x + 7
                            endremoveline = x + 11
                        if listvvv[x] == '"Index" "2"':
                            Inputverify = True
                    log(f"Removelinevar = {removeline}")
                    log(f"Inputverify = {Inputverify}")
                    if Inputverify == True:
                        ptr = 1
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as fr:
                            lines = fr.readlines()
                            ptr = 0
                            with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as fw:
                                for line in lines:
                                    if ptr >= removeline and ptr <= removeline + 5:
                                        pass
                                    else:
                                        fw.write(line)
                                        log(f"PRT = {ptr}, Checking for {removeline} => {removeline + 9}")
                                    ptr += 1
                    
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        listvvv = file.read().replace("\t","").split("\n")
                    for x in range(len(listvvv)):
                        if listvvv[x] == '"Properties"':
                            removeline = x + 7
                        if listvvv[x] == checkfor:
                            Inputverify = True
                    if Inputverify == False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{listvvv[x]}\n")
                            file.write(inputinsert + "\n")
                            for x in range(removeline,len(listvvv)):
                                file.write(f"{listvvv[x]}\n")
                        
                    if Inputverify == True:
                        log("We already have added this type!")
                    
                    


                

            if choicechoice == "Asset Packer":
                assettypechoice = menu(["Models (.MDL)","Instances (.VMF)","Materials (.VTF & .VMT)","Auto Pack (.VTF, .VMT, .MDL)"])
                
                if assettypechoice == "Auto Pack (.VTF, .VMT, .MDL)":
                    autochoice = menu(["Use existing instances found in ucp file","Upload vmf"])
                    if autochoice == "Use existing instances found in ucp file":
                        modellist = []
                        matlist = []
                        #Finds how much vmfs are in there.
                        vmf_files = []
                        files = os.listdir(os.path.join(path,f'package/resources/instances/beepkg/{items[f"{intvalue}_Name"]}/'))
                        for file in files:
                            if file.endswith(".vmf"):
                                vmf_files.append(file)
                        #Reads vmfs and determins if model or material
                        for x in range(len(vmf_files)):
                            with open(os.path.join(path,f'package/resources/instances/beepkg/{items[f"{intvalue}_Name"]}/{items[f"{intvalue}_Name"]}_{x}.vmf'),"r") as file:
                                appendthis = file.read().replace("\t","").split("\n")
                                for x in appendthis:
                                    if len(x) >= 6:
                                        if  '"model"' in x:
                                            modellist.append(x.replace('"model" ',"").replace('.mdl',"").replace('"',''))
                                            log(f"{x} is a model or material!")
                                        else:
                                            log(f"{x} is not a model!")
                                    if len(x) >= 10:
                                        if '"material"' in x:
                                            matlist.append(x.replace('"material" ',"").replace('"',''))
                                            log(f"{x} is a model or material!")
                                        else:
                                            log(f"{x} is not a material!")
                                    else:
                                        log(f"{x} is shorter than 6 and 10!")
                    #Note to self: Make Upload vmf function:
                    removedupe = set(modellist)
                    modellist = list(removedupe)
                    removedupe = set(matlist)
                    matlist = list(removedupe)
                    log(modellist)
                    log(matlist)
                    #Removes duplicates (very common)

                    #being packing
                    p2path = findp2dir()
                    maxdlc = findmaxdlc()
                    warn = 0
                    #Before moving we must make the folders
                    #Find material file + vmt and copy it over to ucp
                    for x in matlist:
                        for y in range(1,maxdlc):
                            checkpath = f'{p2path}/portal2_dlc{y}/materials/{x.replace("//","/")}'
                            if os.path.isfile(checkpath + ".vtf") == True:
                                log(f'{x.split("/")[-1]} is a valid custom material!')
                                #Copy over the material and .vmt
                                destination = checkpath
                                destination.replace(os.path.basename(checkpath),"")
                                if not os.path.exists(os.path.dirname(destination)):
                                    # Create the destination folder
                                    os.makedirs(os.path.dirname(destination))
                                shutil.copyfile(checkpath + ".vtf", path + f"/package/resources/materials/{x}.vtf")
                                shutil.copyfile(checkpath + ".vmt", path + f"/package/resources/materials/{x}.vmt")
                                log(f'Sucesfully packed {x.split("/")[-1]}')
                            else:
                                warn = 1
                                log(f'{x.split("/")[-1]} is not a valid custom material!')
                                log(checkpath)
                    #Model time
                    for x in modellist:
                        for y in range(1,maxdlc):
                            checkpath = f'{p2path}/portal2_dlc{y}/{x.replace("//","/")}'
                            if os.path.isfile(checkpath + ".mdl") == True:
                                log(f'{x.split("/")[-1]} is a valid custom model!')
                                #Copy over the model files
                                destination = path + f"/package/resources/{x}.vmt"
                                destination.replace(os.path.basename(checkpath),"")
                                log(destination)
                                if not os.path.exists(os.path.dirname(destination)):
                                    os.makedirs(os.path.dirname(destination))
                                src_dir = checkpath.replace(os.path.basename(checkpath),"")
                                dst_dir = path + f'/package/resources/{x.replace(os.path.basename(x),"")}'
                                for file in os.listdir(src_dir):
                                    if file.startswith(os.path.basename(checkpath)):
                                        src_path = os.path.join(src_dir, file)
                                        dst_path = os.path.join(dst_dir, file)
                                        shutil.copy2(src_path, dst_path)

                            else:
                                warn = 1
                                log(f'{x.split("/")[-1]} is not a valid custom model!')
                                log(checkpath)
                    print("Operation Completed. (Press Enter)")
                    if warn == 1:
                        print("Some materials / models may not be packed.\nThis may be because it is base textures or they are not found in the dlc folders.")
                    while True:
                        if keyboard.is_pressed("Enter"):
                            break

                if assettypechoice == "Materials (.VTF & .VMT)":
                    if os.path.isdir(os.path.join(path,"Asset_Pack")) == False:
                        os.mkdir(os.path.join(path,"Asset_Pack"))
                    log(f'We have made a folder in {os.path.join(path,"Asset_Pack")}. Please put the .VTF and the .VMT in there.\nNote: We will automatically pack them and the directory will be right\nAnother note: We do not support models!')
                    while True:
                        try:
                            extension1 = os.path.splitext(os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}'))[1]
                        except:
                            pass
                        try:
                            extension2 = os.path.splitext(os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[1]}'))[1]
                        except:
                            pass
                        try:
                            if len(os.listdir(os.path.join(path,"Asset_Pack"))) == 2 and extension1 == ".vmt" or extension1 == ".vtf" and extension2 == ".vmt" or extension2 == ".vtf":
                                break
                        except:
                            pass
                    log(f'Detected File!')
                    log(f'Packing...')
                    readvmt = os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}')
                    if extension1 == ".vmt":
                        readvmt = os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}')
                    elif extension2 == ".vmt":
                        readvmt = os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[1]}')
                    reader = []
                    valueline = ""
                    with open(readvmt,"r") as file2:
                        file2 = file2.read().split("\n")
                    for x in range(len(file2)):
                        reader.append(file2[x].replace("\n","").replace("\t",""))
                        if "$basetexture" in file2[x]:
                            valueline = x

                    if valueline == "":
                        log('Error! No "$basetexture"!')
                    else:
                        readeresult = reader[valueline][14:].replace('"',"").replace(' ',"")
                        readeresult = readeresult.split("/")
                        readeresult2 = []
                        for x in range(len(readeresult) - 1):
                            readeresult2.append(readeresult[x])

                        readeresult = "".join(readeresult2)
                        if os.path.isdir(os.path.join(path,f"package/resources/materials/{readeresult}")) == False:
                            os.mkdir(os.path.join(path,f"package/resources/materials/{readeresult}"))
                        log(f'Moving {os.listdir(os.path.join(path,"Asset_Pack"))[0]}')
                        shutil.move(os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}'), os.path.join(path,f'package/resources/materials/{readeresult}/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}'))
                        log(f'Moving {os.listdir(os.path.join(path,"Asset_Pack"))[0]}')
                        shutil.move(os.path.join(path,f'Asset_Pack/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}'), os.path.join(path,f'package/resources/materials/{readeresult}/{os.listdir(os.path.join(path,"Asset_Pack"))[0]}'))
                        shutil.rmtree(os.path.join(path,"Asset_Pack"))
                    print("Operation Completed. (Press Enter)")
                    while True:
                        if keyboard.is_pressed("Enter"):
                            break
                
                


            if choicechoice == "Input Editor":
                choiceinput = menu(["Add Input","Remove Input","","----------------","Exit to item selector"])
                #Adds input
                if choiceinput == "Exit to item selector":
                    pass
                elif choiceinput == "Add Input":
                    inputinsert = '"BEE2"\n{\n"Type" "AND"\n"Enable_cmd" "input,FireUser1,,0,-1"\n"Disable_cmd" "input,FireUser2,,0,-1"\n}\n'
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        listvvv = file.read().replace("\t","").split("\n")
                    for x in range(len(listvvv)):
                        if listvvv[x] == '"Inputs"':
                            removeline = x + 3
                        if listvvv[x] == '"Enable_cmd"':
                            Inputverify = True
                    if Inputverify == False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{listvvv[x]}\n")
                            file.write(inputinsert + "\n")
                            for x in range(removeline,len(listvvv)):
                                file.write(f"{listvvv[x]}\n")
                        log("Input made. (input,FireUser1,,0,-1),(input,FireUser2,,0,-1)")
                        while True:
                            if keyboard.is_pressed("Enter"):
                                break

                    else:
                        log("Error! There is already an input!")
                        time.sleep(2)
                #Remove input
                elif choiceinput == "Remove Input":
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        listvvv = file.read().replace("\t","").split("\n")
                    for x in range(len(listvvv)):
                        if listvvv[x] == '"Inputs"':
                            removeline = x + 3
                        if listvvv[x] == '"Enable_cmd"':
                            Inputverify = True
                    if Inputverify != False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{listvvv[x]}\n")
                            for x in range(removeline + 8,len(listvvv)):
                                file.write(f"{listvvv[x]}\n")
                        log("Removed Input.")
                        time.sleep(2)
                    else:
                        log("Error! There is already no input!")
                        time.sleep(2)
                else:
                    pass

            if choicechoice == "Output Editor":
                choiceinput = menu(["Add Output","Remove Output","","----------------","Exit to item selector"])
                #Adds output
                if choiceinput == "Exit to item selector":
                    pass
                elif choiceinput == "Add Output":
                    inputinsert = '"BEE2"\n{\n"Type" "AND"\n"out_activate" "instance:Output;OnUser1"\n"out_activate" "instance:Output;OnUser2"\n}\n'
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        listvvv = file.read().replace("\t","").split("\n")
                    for x in range(len(listvvv)):
                        if listvvv[x] == '"Outputs"':
                            removeline = x + 3
                        if listvvv[x] == '"out_activate"':
                            Inputverify = True
                    if Inputverify == False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{listvvv[x]}\n")
                            file.write(inputinsert + "\n")
                            for x in range(removeline,len(listvvv)):
                                file.write(f"{listvvv[x]}\n")
                        log("Output made. (instance:Output;OnUser1),(instance:Output;OnUser2)")
                        while True:
                            if keyboard.is_pressed("Enter"):
                                break
                    else:
                        log("Error! There is already an input!")
                        time.sleep(2)
                #Remove output
                elif choiceinput == "Remove Output":
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        listvvv = file.read().replace("\t","").split("\n")
                    for x in range(len(listvvv)):
                        if listvvv[x] == '"Outputs"':
                            removeline = x + 3
                        if listvvv[x] == '"out_activate"':
                            Inputverify = True
                    if Inputverify != False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{listvvv[x]}\n")
                            for x in range(removeline + 8,len(listvvv)):
                                file.write(f"{listvvv[x]}\n")
                        log("Removed Output.")
                        time.sleep(2)
                    else:
                        log("Error! There is already no input!")
                        time.sleep(2)
                else:
                    pass
            
            #Remove item
            if choicechoice == "Remove Item":
                with open(os.path.join(path, "package/info.txt")) as file:
                    listvvv = file.read().replace("\t","").split("\n")

                locationvar = f'{intvalue}_ID'

                for x in range(len(listvvv)):
                    if listvvv[x] == f'"ID"  "{items[locationvar][1:]}"':
                        removeline = x + 1
                
                def delline(linev):
                    with open(os.path.join(path, "package/info.txt"), 'r') as fr:
                        lines = fr.readlines()
                        ptr = 1
                        with open(os.path.join(path, "package/info.txt"), 'w') as fw:
                            for line in lines:                
                                if ptr != linev:
                                    fw.write(line)
                                ptr += 1

                #Removing lines
                for x in range(11):
                    delline(removeline - 2)
                log(f'Removed item in info.txt. ({items[locationvar].replace(" ","")})')
                try:
                    shutil. rmtree(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}'))
                except:
                    pass
                log(f'Removed item in items folder. ({items[locationvar].replace(" ","")})')
                try:
                    shutil. rmtree(os.path.join(path, f'package/resources/instances/beepkg/{items[str(intvalue) + "_Name"]}'))
                except:
                    pass
                try:
                    os.remove(os.path.join(path, f'package/resources/BEE2/items/beepkg/{items[str(intvalue) + "_Name"]}'))
                except:
                    pass
                try:
                    os.remove(os.path.join(path, f'package/resources/materials/models/props_map_editor/palette/beepkg/{items[str(intvalue) + "_Name"]}'))
                except:
                    pass
                log(f'Removed item in resources folder. ({items[f"{intvalue}_Name"]})')
                log(f'Removed item. ({items[f"{intvalue}_Name"]})')
            else:
                pass

    else:
        
        log("Error! No info.txt!")
        time.sleep(2)
        shutil.rmtree(os.path.join(path,"package"))
        if os.path.isdir(os.path.join(path,"package")) == False:
            os.mkdir(os.path.join(path,"package"))
        log("Deleted packages.")
        return

print("Welcome to Areng's Beemod Package Editor!\nDisclaimer: This does not make packages. This just simply packs textures and writes vbsp_configs.\nAnother note: This only works on beepkg's completed packages")
print("When ready please upload a link to the terminal.")
print(
    "We highly recommend you uploading the package to discord and copying the download link and sending it here."
)
dev_index = version.index("_DEV")
dev_string = version[dev_index:]
if dev_string != "_DEV":
    if requests.get("https://versioncontrol.orange-gamergam.repl.co/api/bpe").json() == version:
        print("No updates are currently available.")
    else:
        print(f'There is an update available. You are using ({version}) Newest is ({requests.get("https://versioncontrol.orange-gamergam.repl.co/api/bpe").json()})')
        print("You can get the update here https://github.com/Areng14/BeePackageEditor/releases")
        time.sleep(5)
        webopen("https://github.com/Areng14/BeePackageEditor/releases")
        while True:
            if keyboard.is_pressed("Enter"):
                break
if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
    using = "__file__"
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")
    using = "sys.executable"
downloadlink = input()
url = downloadlink
r = requests.get(url, allow_redirects=True)
open(downloadlink[78:], 'wb').write(r.content)

#Clears packages folder
try:
    shutil.rmtree(os.path.join(path,"packages"))
except:
    pass
#Downloads package
base = os.path.splitext(downloadlink[78:])[0]
if os.path.splitext(downloadlink[78:])[1] != ".zip":
    os.rename(downloadlink[78:], base + '.zip')
if os.path.isdir(os.path.join(path,"package")) == False:
    os.mkdir(os.path.join(path,"package"))
if os.path.isdir(os.path.join(path,"output")) == False:
    os.mkdir(os.path.join(path,"output"))
if os.path.isdir(os.path.join(path,"logs")) == False:
    os.mkdir(os.path.join(path,"logs"))
#Changing extension to .zip

with zipfile.ZipFile(downloadlink[78:-9] + ".zip", 'r') as zip_ref:
    zip_ref.extractall(os.path.join(path,"package"))
os.remove(downloadlink[78:-9] + ".zip")
#Unzipping

for x in range(100):
    print("\n")

main()

print("Thanks for using Beemod Package Editor!")
time.sleep(60)
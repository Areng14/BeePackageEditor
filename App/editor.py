import menu
import os
import shutil
import time    

def main():
    timev = time.time()
    def clear():
        for x in range(100):
            log("\n")

    def log(text):
        with open(os.path.join(path,f"logs/BPE_LOG[{timev}].txt"), 'a') as file:
            file.write(str(text) + "\n")
            print(text)

    path = __file__.replace(os.path.basename(__file__),"")
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

            #Start a menu
            while True:
                menulist = []
                for x in range(round(len(items) / 3)):
                    menulist.append(items.get(f"{x + 1}_NameS")[:1].upper() + items.get(f"{x + 1}_NameS")[1:])
                menulist.append("")
                menulist.append(r"---------{Utilities}---------")
                menulist.append("Exit")
                menulist.append("Pack")
                itemchoice = menu.menu(menulist)

                #Starts listening for utility buttons
                if itemchoice == "":
                    pass
                if itemchoice == r"---------{Utilities}---------":
                    pass
                if itemchoice == "Exit":
                    time.sleep(1)
                    shutil.rmtree(os.path.join(path,"package"))
                    if os.path.isdir(os.path.join(path,"package")) == False:
                        os.mkdir(os.path.join(path,"package"))
                    return
                if itemchoice == "Pack":
                    ID = info["Name"].replace("'","").replace(" ","_").replace('"',"")[1:]
                    shutil.make_archive(ID, 'zip',os.path.join(path, "package"))
                    base = os.path.splitext(ID)[0]
                    os.rename(ID + ".zip", base + '.bee_pack')
                    shutil.move(path + ID + ".bee_pack",os.path.join(path, "output/" + ID + ".bee_pack"))
                    log("Operation Completed.")
                else:
                    break

            #Converting item choice to int
            for x in range(round(len(items) / 3)):
                if items[f"{x + 1}_NameS"] == itemchoice.lower():
                    intvalue = x + 1
                    break
            log("intvalue = " + str(intvalue))


            #Start a menu to choose what to do

            choicechoice = menu.menu(["Allow for cube colorizer colors ($color)","Add Types","Asset Packer","Remove Item","Input Editor","Output Editor","","----------------","Back"])
            #Add/Remove input
            if choicechoice == "Back":
                pass
            
            if choicechoice == "Add Types":
                choice = menu.menu(["Timer Type","Cube Type","Button Type","Start Enabled","Start Reversed","","----------------","Back"])
                datafile = False
                if choice == "Timer Type":
                    inputinsert = '"TimerDelay"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "TimerDelay"
                    datafile = "data/Timerdata.bpe_data"
                if choice == "Cube Type":
                    inputinsert = '"CubeType"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "CubeType"
                    datafile = "data/Cubedata.bpe_data"
                if choice == "Button Type":
                    inputinsert = '"ButtonType"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "ButtonType"
                    datafile = "data/Buttondata.bpe_data"
                if choice == "Start Enabled":
                    inputinsert = '"StartEnabled"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "StartEnabled"
                    datafile = "data/Enabledata.bpe_data"
                if choice == "Start Reversed":
                    inputinsert = '"StartReversed"\n{\n"DefaultValue" "1"\n"Index" "2"\n}'
                    checkfor = "StartReversed"
                    datafile = "data/Reversedata.bpe_data"
                if datafile != False:
                    with open(os.path.join(path,datafile),"r") as file:
                        listv = file.read().replace("\t","").split("\n")
                    num = 0
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
                        list = file.read().replace("\t","").split("\n")
                    for x in range(len(list)):
                        if list[x] == '"Properties"':
                            removeline = x + 7
                            endremoveline = x + 11
                        if list[x] == '"Index" "2"':
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
                        list = file.read().replace("\t","").split("\n")
                    for x in range(len(list)):
                        if list[x] == '"Properties"':
                            removeline = x + 7
                        if list[x] == checkfor:
                            Inputverify = True
                    if Inputverify == False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{list[x]}\n")
                            file.write(inputinsert + "\n")
                            for x in range(removeline,len(list)):
                                file.write(f"{list[x]}\n")
                        
                    if Inputverify == True:
                        log("We already have added this type!")
                    
                    


                

            if choicechoice == "Asset Packer":
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
                log("Operation Completed.")
                time.sleep(2)
                
                


            if choicechoice == "Input Editor":
                choiceinput = menu.menu(["Add Input","Remove Input","","----------------","Exit to item selector"])
                #Adds input
                if choiceinput == "Exit to item selector":
                    pass
                elif choiceinput == "Add Input":
                    inputinsert = '"BEE2"\n{\n"Type" "AND"\n"Enable_cmd" "input,FireUser1,,0,-1"\n"Disable_cmd" "input,FireUser2,,0,-1"\n}\n'
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        list = file.read().replace("\t","").split("\n")
                    for x in range(len(list)):
                        if list[x] == '"Inputs"':
                            removeline = x + 3
                        if list[x] == '"Enable_cmd"':
                            Inputverify = True
                    if Inputverify == False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{list[x]}\n")
                            file.write(inputinsert + "\n")
                            for x in range(removeline,len(list)):
                                file.write(f"{list[x]}\n")
                        log("Input made. (input,FireUser1,,0,-1),(input,FireUser2,,0,-1)")
                        time.sleep(2)
                    else:
                        log("Error! There is already an input!")
                        time.sleep(2)
                #Remove input
                elif choiceinput == "Remove Input":
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        list = file.read().replace("\t","").split("\n")
                    for x in range(len(list)):
                        if list[x] == '"Inputs"':
                            removeline = x + 3
                        if list[x] == '"Enable_cmd"':
                            Inputverify = True
                    if Inputverify != False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{list[x]}\n")
                            for x in range(removeline + 8,len(list)):
                                file.write(f"{list[x]}\n")
                        log("Removed Input.")
                        time.sleep(2)
                    else:
                        log("Error! There is already no input!")
                        time.sleep(2)
                else:
                    pass

            if choicechoice == "Output Editor":
                choiceinput = menu.menu(["Add Output","Remove Output","","----------------","Exit to item selector"])
                #Adds output
                if choiceinput == "Exit to item selector":
                    pass
                elif choiceinput == "Add Output":
                    inputinsert = '"BEE2"\n{\n"Type" "AND"\n"out_activate" "instance:Output;OnUser1"\n"out_activate" "instance:Output;OnUser2"\n}\n'
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        list = file.read().replace("\t","").split("\n")
                    for x in range(len(list)):
                        if list[x] == '"Outputs"':
                            removeline = x + 3
                        if list[x] == '"out_activate"':
                            Inputverify = True
                    if Inputverify == False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{list[x]}\n")
                            file.write(inputinsert + "\n")
                            for x in range(removeline,len(list)):
                                file.write(f"{list[x]}\n")
                        log("Output made. (instance:Output;OnUser1),(instance:Output;OnUser2)")
                        time.sleep(2)
                    else:
                        log("Error! There is already an input!")
                        time.sleep(2)
                #Remove output
                elif choiceinput == "Remove Output":
                    filecontent = []
                    leng = 0
                    Inputverify = False
                    with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"r") as file:
                        list = file.read().replace("\t","").split("\n")
                    for x in range(len(list)):
                        if list[x] == '"Outputs"':
                            removeline = x + 3
                        if list[x] == '"out_activate"':
                            Inputverify = True
                    if Inputverify != False:
                        with open(os.path.join(path, f'package/items/{items[f"{intvalue}_Name"]}/editoritems.txt'),"w") as file:
                            for x in range(removeline):
                                file.write(f"{list[x]}\n")
                            for x in range(removeline + 8,len(list)):
                                file.write(f"{list[x]}\n")
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
                    list = file.read().replace("\t","").split("\n")

                locationvar = f'{intvalue}_ID'

                for x in range(len(list)):
                    if list[x] == f'"ID"  "{items[locationvar][1:]}"':
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
        
        log("Error! No info.txt!")
        time.sleep(2)
        shutil.rmtree(os.path.join(path,"package"))
        if os.path.isdir(os.path.join(path,"package")) == False:
            os.mkdir(os.path.join(path,"package"))
        log("Deleted packages.")
        return


if __name__ == "__main__":
    main()
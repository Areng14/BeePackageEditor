import os
import zipfile
import srctools
import numpy as np
import subprocess
from PIL import Image
import sys

#Initiating program and varibles

#Finds the correct path to the .exe or the .py file
if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

#Makes directories
dirs = ["packages","logs","config"]
for dirs in dirs:
    try:
        os.makedirs(os.path.join(path,dirs))
    except FileExistsError:
        pass

#Declaring varibles
packagesdir = os.path.join(path,"packages")
beepkg = 0
items = {}
#Make directories

def removeformat(text):
    replacethis = ["\t","\n"]
    for x in replacethis:
        text = text.replace(x,"")
    return text

def readvmf(path_to_vmf,mode):
    returndict = {"Model":"","Material":"","Sound":"","Script":""}
    modellist,matlist,soundlist,vscriptlist = [],[],[],[]
    supportedextensions = [".MP3",".WAV"]
    with open(path_to_vmf,"r") as vmf:
        #Store in a list
        vmflines = vmf.read().replace("\t","").replace(" ","").split("\n")
    #Get details
    for lines in vmflines:
        if "MODEL" in mode.upper():
            if '"MODEL"' in lines.upper():
                modellist.append(lines.upper().replace('"MODEL"','').replace(' ','').replace('"',''))
        if "MATERIAL" in mode.upper():
            if '"MATERIAL"' in lines.upper():
                matlist.append("materials/" + lines.upper().replace('"MATERIAL"','').replace(' ','').replace('"',''))
        if "SOUND" in mode.upper():
            if '"MESSAGE"' in lines.upper():
                #Check if its a sound file or not
                if os.path.splitext(os.path.basename(lines.upper().replace('"MESSAGE"','').replace('"','')))[1] in supportedextensions:
                    soundlist.append("sound/" + lines.upper().replace('"MESSAGE"','').replace(' ','').replace('"',''))
        if "SCRIPT" in mode.upper():
            if '"VSCRIPTS"' in lines.upper():
                vscriptlist.append("scripts/vscripts" + lines.upper().replace('"VSCRIPTS"','').replace(' ','').replace('"',''))
    #Compile them together
    returndict["Model"] = list(set(modellist))
    returndict["Material"] = list(set(matlist))
    returndict["Sound"] = list(set(soundlist))
    returndict["Script"] = list(set(vscriptlist))
    return returndict


def patch_vtfs(item_dict):
    leng = item_dict["info"]
    for x in range(leng[0]):
        ilist = item_dict[x]
        ilist = ilist[2]
        #Get the item path (ilist)
        with open(os.path.join(packagesdir,"items/",ilist,"properties.txt")) as prop:
            pathtoimgl = prop.read().replace("\t","").split("\n")
        for x in range(len(pathtoimgl)):
            if '"ICON"' in pathtoimgl[x].upper():
                x += 2
                break
        #Cycle through pathtoimg to find the path to the img

        pathtoimg = os.path.join(packagesdir,"resources/BEE2/items",pathtoimgl[x].replace('"0" ',"").replace('"',""))
        #Gets the path ONLY

        vtfpath = os.path.join(packagesdir,"resources/materials/models/props_map_editor/palette",pathtoimgl[x].replace('"0" ',"").replace('"',"").replace(os.path.basename(pathtoimgl[x].replace('"0" ',"").replace('"',"")),""),os.path.splitext(os.path.basename(pathtoimgl[x].replace('"0" ',"").replace('"',"")))[0] + ".vtf")

        #Thanks to pee too see ee guys they made a vtf converter we will run it with os.system()

        extension = str(os.path.splitext(os.path.basename(pathtoimgl[x].replace('"0" ',"").replace('"',"")))[1])[1:]

        name = os.path.splitext(os.path.basename(pathtoimgl[x].replace('"0" ',"").replace('"',"")))[0]
        
        pathtoimg = pathtoimg.replace("\\","/")

        #Patching image

        first_image = Image.new("RGB", (128, 128), (255, 255, 255))

        second_image = Image.open(pathtoimg)

        second_image = second_image.resize((128, 128), Image.ANTIALIAS)

        first_image.paste(second_image, (0, 0))

        first_image.save(pathtoimg)

        print(f'vtex2 convert -f dxt5 "{pathtoimg}"')
        os.system(f'vtex2 convert --version 7.2 -f dxt5 "{pathtoimg}"')
        os.remove(vtfpath)
        os.rename(pathtoimg.replace(os.path.basename(pathtoimg),os.path.splitext(os.path.basename(pathtoimg))[0] + ".vtf"),vtfpath)
        #VTF not working properly for some reason

def readfile(file):
    #Checks if file exists before extracting. If so remove contents
    items = {}
    #Extracting the zip
    try:
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(packagesdir)
    except PermissionError:
        raise "NoPerms"
    except FileNotFoundError:
        raise "NonExistant"
    #Begin to read info.txt and return information collected into a dict. Format: {INT: ID, Name, iteminfo path}
    with open(os.path.join(packagesdir,"info.txt")) as infotxt:
        linelist = infotxt.read().split("\n")
        #^Seperating info.txt into lists via each enter
        if linelist[0] == "// Generated by ComponentBase.BeePackage.export":
            beepkg = 1
        #Detects if file is made with beepkg or not
        
        counter2 = 0
        counter = 0
        idcheck,namecheck = 0,0
        for line in linelist:
            if '"ID"' in removeformat(line.upper()) and idcheck == 0:
                pakid = removeformat(line.upper()).replace('"ID"',"").replace('"',"")
                idcheck = 1
            if '"NAME"' in removeformat(line.upper()) and namecheck == 0:
                pakname = removeformat(line.upper()).replace('"NAME"',"").replace('"',"")
                namecheck = 1
            if removeformat(line.upper()) == '"ITEM"':
                itemid,itemconfig,itemname = "","",""
                #We have detected an item now we will read the thing
                for x in range(counter,len(linelist)):
                    if '"ID"' in removeformat(linelist[x].upper()):
                        itemid = linelist[x].replace(" ","").replace('"ID"',"").replace("\t","").replace('"',"").replace("'","")
                    if '"BEE2_CLEAN"' in removeformat(linelist[x].upper()):
                        itemconfig = linelist[x].replace(" ","").replace('"BEE2_CLEAN"',"").replace("\t","").replace('"',"").replace("'","")
                    if itemid and itemconfig:
                        break
                #Get name of item
                with open(os.path.join(packagesdir,"items",removeformat(itemconfig),"editoritems.txt"),"r") as editorfile:
                    editlinelist = editorfile.read().split("\n")
                    for x in range(len(editlinelist)):
                        if '"NAME"' in removeformat(editlinelist[x]).upper():
                            itemname = editlinelist[x].replace('"Name"',"").replace("\t","").replace('"',"").replace("'","").replace("  ","")
                            break
                items[counter2] = [itemid,itemname,itemconfig]
                counter2 += 1
            counter += 1
        #Goes over info.txt and finds inportant info
        #Finishing up the read and will be adding some package info to the dict
        items["info"] = [counter2,beepkg,pakid,pakname]
    #^ Trys to extract the zip. If fails it returns "Invalid File"
    return items
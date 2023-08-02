import os
import sys
import srctools
import shutil
import traceback
from PIL import Image
import assetmanager
import requests

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

def makedir(dir):
    try:
        os.makedirs(dir)
    except FileExistsError:
        pass

"""
Generation checklist

C: Properties.txt
C: Editoritems.txt
C: Image
C: VTF
C: Instance
C: Info.txt
"""

def makevtf(pathtopng) -> str:
    """
    Makes a vtf from the image
    """

    VTFTarget = Image.open(pathtopng)
    width, height = VTFTarget.size
    vtf = srctools.VTF(width, height)
    vtf.get().copy_from(VTFTarget.tobytes())
    vtf_path = os.path.join(path,pathtopng.replace(os.path.basename(pathtopng), ""),os.path.splitext(os.path.basename(pathtopng))[0]+".vtf")
    with open(vtf_path, "wb") as f:
        vtf.save(f)
    return vtf_path

def makeitem(item_info,dir) -> bool:
    """
    Requires a package to be made before running
    Make sure dir is the package dir
    """
    Itemname = item_info["Name"]
    Itemid = Itemname.lower().replace(" ","_")
    ItemidU = Itemname.upper().replace(" ","_")
    Itemdesc = item_info["Description"].split("\n")
    Iteminst = item_info["Instance"]
    Itemicon = item_info["Icon"]
    Author = ", ".join(item_info["Author"])

    try:
        #Begin making package
        #Make dirs
        makedir(os.path.join(dir,"items",Itemid))
        makedir(os.path.join(dir,"resources","BEE2","items","beepkg"))
        makedir(os.path.join(dir,"resources","instances","beepkg",Itemid))
        makedir(os.path.join(dir,"resources","materials","models","props_map_editor","palette","beepkg"))

        #Make editoritems.txt

        #Get template editoritems.txt
        request = requests.get("https://versioncontrol.areng123.repl.co/file/editoritems.txt")
        editoritems = request.text

        #Fill placeholders
        placeholders = {
            "ITEM_NAME_UPPER" : ItemidU,
            "ITEM_NAME" : ItemidU,
            "Item_Name" : Itemname,
            "item_name" : Itemid,
            "Author_Name" : Author,
        }

        for placeholder, value in placeholders.items():
            editoritems = editoritems.replace(placeholder, str(value))

        with open(os.path.join(dir,"items",Itemname.lower().replace(" ","_"),"editoritems.txt"),"w") as editor:
            editor.write(editoritems)

        #Add thing to info.txt
        request = requests.get("https://versioncontrol.areng123.repl.co/file/info.txt")
        info = request.text

        for placeholder, value in placeholders.items():
            info = info.replace(placeholder, str(value))

        with open(os.path.join(dir,"info.txt"),"a") as infof:
            infof.write(info)

        #Write properties.txt
        request = requests.get("https://versioncontrol.areng123.repl.co/file/properties.txt")
        properties = request.text

        #Fill placeholders

        insertdescription = []
        for index,line in enumerate(Itemdesc):
            if index != len(Itemdesc) - 1:
                insertdescription.append(f'\t\t"" "{line}"\n')
            else:
                insertdescription.append(f'\t\t"" "{line}"')

        placeholders['description_temp'] = ''.join(insertdescription)

        for placeholder, value in placeholders.items():
            properties = properties.replace(placeholder, str(value))

        with open(os.path.join(dir,"items",Itemname.lower().replace(" ","_"),"properties.txt"),"w") as prop:
            prop.write(properties)

        #Copy images
        shutil.copyfile(Itemicon,os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}.png"))
        #Edit image
        image = Image.open(os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}.png"))
        resized_image = image.resize((64, 64))
        resized_image.save(os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}.png"))

        #Make VTF
        #Copy images
        shutil.copyfile(Itemicon,os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}vtf.png"))
        #Edit image
        image = Image.open(os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}vtf.png"))
        resized_image = image.resize((128, 128))
        resized_image.save(os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}vtf.png"))

        vtfpath = makevtf(os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}vtf.png"))
        os.rename(vtfpath,os.path.join(dir,"resources","materials","models","props_map_editor","palette","beepkg",f"{Itemid}.vtf"))
        os.remove(os.path.join(dir,"resources","BEE2","items","beepkg",f"{Itemid}vtf.png"))

        #Add instance
        shutil.copyfile(Iteminst,os.path.join(dir,"resources","instances","beepkg",Itemid,f"{Itemid}_0.vmf"))

        return True

    except Exception as error:
        print(traceback.format_exc())

item = makeitem(iteminfo,os.path.join("testing","pkg"))

if item:
    print("Item creation sucesfull")
else:
    print("Item creation failed")
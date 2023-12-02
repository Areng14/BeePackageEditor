import os
import subprocess
import sys

def open_with_default_editor(filepath):
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin":
            subprocess.call(["open", filepath])
        elif sys.platform == "linux":
            subprocess.call(["xdg-open", filepath])
        else:
            print(f"Unsupported platform: {sys.platform}")
    except Exception as e:
        print(f"Failed to open file: {e}")

vbsp = os.path.join(packagemanager.packagesdir,"items",item[2],"vbsp_config.cfg")

if not os.path.isfile(os.path.join(packagemanager.packagesdir,"items",item[2],"vbsp_config.cfg")):
    with open(os.path.join(packagemanager.packagesdir,"items",item[2],"vbsp_config.cfg"),"w") as vvbsp:
        vvbsp.write("")
assetmanager.format_file(os.path.join(packagemanager.packagesdir,"items",item[2],"vbsp_config.cfg"))
open_with_default_editor(vbsp)
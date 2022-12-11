import zipfile
import os
import shutil
import editor
import requests
import time
import menu



print("Welcome to Areng's Beemod Package Editor!\nDisclaimer: This does not make packages. This just simply packs textures and writes vbsp_configs.\nAnother note: This only works on beepkg's completed packages")
print("When ready please upload a link to the terminal.")
print(
    "We highly recommend you uploading the package to discord and copying the download link and sending it here."
)
path = __file__.replace(os.path.basename(__file__),"")
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
if os.path.isdir(os.path.join(path,"data")) == False:
    os.mkdir(os.path.join(path,"logs"))
#Changing extension to .zip

with zipfile.ZipFile(downloadlink[78:-9] + ".zip", 'r') as zip_ref:
    zip_ref.extractall(os.path.join(path,"package"))
os.remove(downloadlink[78:-9] + ".zip")
#Unzipping

for x in range(100):
    print("\n")

editor.main()

print("Thanks for using Beemod Package Editor!")
time.sleep(60)
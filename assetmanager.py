#Manage assets

import srctools.game
import srctools.packlist
import os
import json
import re
import requests

def finedepen(mdlfile,p2dir) -> list:
    """
    Find a model's material dependencies
    """
    gamefile = os.path.join(p2dir,"portal2")
    game = srctools.game.Game(gamefile)
    fsys = game.get_filesystem()
    packlist = srctools.packlist.PackList(fsys)
    packlist.pack_file(mdlfile)
    packlist.eval_dependencies()

    # Get a list of required files
    returnlist = []
    for packfile in packlist._files:
        if packfile[:9].upper() == "materials".upper():
            returnlist.append(os.path.splitext(packfile)[0])
    return returnlist

def find_blocks(text, key, pattern=r'{key}\n{{(.*?)}}') -> list:
    """
    Find a block in code
    """
    escaped_key = re.escape(key)
    pattern = re.compile(pattern.format(key=escaped_key), re.DOTALL)

    matches = re.findall(pattern, text)
    if matches:
        return [match.replace('\t', '') for match in matches]
    else:
        return None

def vtext_to_json(text) -> dict:
    """
    Converts vtext to a json
    """
    props = {}
    lines = text.strip().split('\n')[2:-1]
    for line in lines:
        values = line.strip().split()
        if len(values) >= 2:
            key, value = values
            key = key.strip('"')
            value = value.strip('"')
            props[key] = value
    return {text.split('\n')[0] : props}
#/\ Made to make dealing with editoritems.txt easier
#\/ Made to make dealing with editoritems.txt easier
def json_to_vtext(json) -> str:
    """
    Converts json to vtext
    """
    text = ''
    key = list(json.keys())[0]
    props = json[key]
    text += f'{key}\n'
    text += '{\n'
    for prop_key, prop_value in props.items():
        text += f'    {prop_key}\n'
        text += '    {\n'
        if isinstance(prop_value, dict):
            for k, v in prop_value.items():
                text += f'        "{k}"\t"{v}"\n'
        else:
            text += f'        {prop_value}\n'
        text += '    }\n'
    text += '}'
    return text

def writeconfig(key,value):
    global config
    """
    Writes to the config
    """
    config[key] = value
    with open(os.path.join(os.getenv('APPDATA'),"BPE","config.cfg"),"w") as fconfig:
        fconfig.write(json.dumps(config))

def findvalue(text,key) -> list:
    """
    Finds a value of a key
    """
    pattern = re.compile(r'{}\n{{(.*?)}}'.format(key))
    return re.findall(pattern, text)
    
def getdata(data) -> str:
    response = requests.get(f"https://versioncontrol.areng123.repl.co/{data}")
    return response.text

def format_string(string) -> str:
    """
    Formats a string
    """
    content = string.splitlines()
    indent = 0
    formatted_content = []
    for line in content:
        if "{" in line:
            indent += 1
        formatted_line = "\t" * indent + line.strip()
        formatted_content.append(formatted_line)
        if "}" in line:
            indent -= 1
    return "\n".join(formatted_content)

def format_file(file_path):
    """
    Formats a file
    """
    with open(file_path, "r") as file:
        content = file.readlines()
    indent = 0
    formatted_content = []
    for line in content:
        if "{" in line:
            indent += 1
        formatted_line = "\t" * indent + line.strip()
        formatted_content.append(formatted_line)
        if "}" in line:
            indent -= 1
    with open(file_path, "w") as file:
        file.write("\n".join(formatted_content))

config = {}

def loadconfig():
    global config
    appdata_path = os.path.join(os.getenv('APPDATA'), "BPE")
    config_path = os.path.join(appdata_path, "config.cfg")

    if not os.path.isdir(appdata_path):
        os.makedirs(appdata_path)

    if not os.path.isfile(config_path):
        config = {
            "package": "",
            "plugins": [],
            "theme": 0
        }
        with open(config_path, "w") as fconfig:
            json.dump(config, fconfig)
    else:
        with open(config_path, "r") as fconfig:
            try:
                config = json.load(fconfig)
            except json.JSONDecodeError:
                config = {
                    "package": "",
                    "plugins": [],
                    "theme": 0
                }
                with open(config_path, "w") as f_write:
                    json.dump(config, f_write)

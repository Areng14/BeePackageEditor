#Manage assets

import srctools.game
import srctools.packlist
import os
import re
import requests

def finedepen(mdlfile,p2dir):
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

def find_blocks(text, key, pattern=r'{key}\n{{(.*?)}}'):
    escaped_key = re.escape(key)
    pattern = re.compile(pattern.format(key=escaped_key), re.DOTALL)

    matches = re.findall(pattern, text)
    if matches:
        return [match.replace('\t', '') for match in matches]
    else:
        return None

def vtext_to_json(text):
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
def json_to_vtext(json):
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




def findvalue(text,key):
    pattern = re.compile(r'{}\n{{(.*?)}}'.format(key))
    return re.findall(pattern, text)
    
def getdata(data):
    response = requests.get(f"https://versioncontrol.areng123.repl.co/{data}")
    return response.text

def format_string(string):
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

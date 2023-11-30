import time
import os
import sys

if os.path.basename(sys.executable) == "python.exe":
    path = __file__.replace(os.path.basename(__file__),"")
else:
    path = sys.executable.replace(os.path.basename(sys.executable),"")

filename = os.path.join(path, "logs", str(time.time()) + ".txt")

def logerror(msg):
    with open(filename,"a") as file:
        file.write("[ERROR] " + str(msg) + "\n")
    print("[ERROR] " + str(msg))

def loginfo(msg):
    with open(filename,"a") as file:
        file.write("[INFO] " + str(msg) + "\n")
    print("[INFO] " + str(msg))

def log(msg):
    with open(filename,"a") as file:
        file.write(str(msg) + "\n")
    print(str(msg))

def logwarn(msg):
    with open(filename,"a") as file:
        file.write("[WARNING!] " + str(msg) + "\n")
    print("[WARNING!] " + str(msg))

print(filename)
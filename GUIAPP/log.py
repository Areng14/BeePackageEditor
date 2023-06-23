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
        file.write("[ERROR] " + msg + "\n")
    print("[ERROR] " + msg)

def loginfo(msg):
    with open(filename,"a") as file:
        file.write("[INFO] " + msg + "\n")
    print("[INFO] " + msg)

def log(msg):
    with open(filename,"a") as file:
        file.write(msg + "\n")
    print(msg)

def logwarn(msg):
    with open(filename,"a") as file:
        file.write("[WARNING!] " + msg + "\n")
    print("[WARNING!] " + msg)

print(filename)
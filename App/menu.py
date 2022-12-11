import sys
import keyboard
import time
from colorama import Fore, Style, init
from math import ceil

def inputnew(prompt):
    return input(prompt)


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
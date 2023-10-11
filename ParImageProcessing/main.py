from Processing import *

import curses
import time

currentMenu = "main" # main menu

settingsAccepted = set()
settingsAccepted.add("Sharpen")
settingsAccepted.add("Sepia")

sizeAccepted = (0, 0, 0)
tmp = ""
userInput = "img"
userOutput = "wow"
enableInput = False
enableOutput = False

enableSaving = False


isQuit = False
def menuView(stdscr):
    # console settings
    curses.curs_set(0) # no cursor
    stdscr.nodelay(1)  # make getch() unblocked
    global currentMenu
    global settingsAccepted
    global sizeAccepted
    global tmp
    global userInput
    global userOutput
    global enableInput
    global enableOutput
    global enableSaving
    global isQuit

    while True:
        # getting keys
        key = stdscr.getch()
        if (not enableOutput) and (not enableInput) and (key == ord("q")):
            isQuit = True
            break

        if currentMenu == "main":
            if key == ord("1"):
                currentMenu = "Settings"
                stdscr.clear()
            elif key == ord("2"):
                currentMenu = "Save"
                enableSaving = True
                stdscr.clear()
        elif currentMenu == "Resize":         
            # resize menu
            if key == ord("1"):
                sizeAccepted = (800, 600, 1)
            elif key == ord("2"):
                sizeAccepted = (1280, 720, 2)
            elif key == ord("3"):
                sizeAccepted = (0, 0, 0)
            elif key == ord("4"):
                sizeAccepted = (4096, 4096, 4)

            elif key == ord("z"):
                currentMenu = "Settings"
                stdscr.clear()
        elif currentMenu != "main":
            # getting user input/output if needed
            if enableInput or enableOutput:
                if key == 10:
                    curses.noecho()
                    if enableInput:
                        userInput = tmp
                        enableInput = False
                    if enableOutput:
                        userOutput = tmp
                        enableOutput = False
                    tmp = ""
                    stdscr.clear()
                elif key != -1:
                    tmp += chr(key)
                continue

            if key == ord("z"):
                currentMenu = "main"
                stdscr.clear()

            # Input user folder with images
            if key == ord("1"):
                curses.echo()
                enableInput = True
            elif key == ord("2"):
                curses.echo()
                enableOutput = True

            # Enable filters if needed
            elif key == ord("3"):
                if "Sepia" in settingsAccepted:
                    settingsAccepted.remove("Sepia")
                else:
                    settingsAccepted.add("Sepia")
            elif key == ord("5"):
                currentMenu = "Resize"
                stdscr.clear()
            elif key == ord("4"):
                if "Sharpen" in settingsAccepted:
                    settingsAccepted.remove("Sharpen")
                else:
                    settingsAccepted.add("Sharpen")
                    
        # Drawing current menu
        if currentMenu == "main":
            stdscr.addstr(0, 0, "1. Settings")
            stdscr.addstr(1, 0, "2. Save")
        elif currentMenu == "Resize":
            if sizeAccepted[2] == 1:
                stdscr.addstr(0, 0, "1. 800x600", curses.A_BOLD)
            else:
                stdscr.addstr(0, 0, "1. 800x600")
            if sizeAccepted[2] == 2:
                stdscr.addstr(1, 0, "2. 1280x720", curses.A_BOLD)
            else:
                stdscr.addstr(1, 0, "2. 1280x720")
            if sizeAccepted[2] == 0:
                stdscr.addstr(2, 0, "3. Do not change", curses.A_BOLD)
            else:
                stdscr.addstr(2, 0, "3. Do not change")
            if sizeAccepted[2] == 4:
                stdscr.addstr(3, 0, "4. 4096x4096", curses.A_BOLD)
            else:
                stdscr.addstr(3, 0, "4. 4096x4096")
        elif currentMenu == "Settings":
            stdscr.addstr(0, 0, f"1. Input folder: {userInput}")
            stdscr.addstr(1, 0, f"2. Output folder: {userOutput}")
            if "Sepia" in settingsAccepted:
                stdscr.addstr(2, 0, "3. Sepia", curses.A_BOLD)
            else:
                stdscr.addstr(2, 0, "3. Sepia")
            if "Sharpen" in settingsAccepted:
                stdscr.addstr(3, 0, "4. Sharpen", curses.A_BOLD)
            else:
                stdscr.addstr(3, 0, "4. Sharpen")
            stdscr.addstr(4, 0, "5. Resize")

            if enableInput: 
                stdscr.addstr(12, 0, f"Enter accurate input folder name")
                stdscr.addstr(13, 3, tmp)
            
            if enableOutput:
                stdscr.addstr(12, 0, f"Enter accurate output folder name")
                stdscr.addstr(13, 3, tmp)

        elif currentMenu == "Save": 
            break
        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(menuView)
    if not isQuit:
        start = time.time()
        processImages(userInput, userOutput, size=(sizeAccepted[0], sizeAccepted[1]), 
                        sepia=("Sepia" in settingsAccepted),
                        sharpened=("Sharpen" in settingsAccepted))
        end = time.time()
        print(f"TIME: {end - start} s")
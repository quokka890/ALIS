import os
import sys
import atexit

if os.path.exists("logs.txt") == True:
    os.remove("logs.txt")

def cleanup(Called_By_AtExit=True, ExitCode=0):
    if exit == 0: 
        return
    elif os.path.exists("config.json"):
        os.remove("config.json")
        s = os.path.exists("config.json")
    if Called_By_AtExit == False:
        exit(ExitCode)

atexit.register(cleanup)
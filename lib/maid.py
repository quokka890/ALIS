import os
import sys
import atexit

def cleanup():
    if exit(1): 
        return
    else:
        print("cleaning up")
        os.remove("config.json")
        s = os.path.exists("config.json")

atexit.register(cleanup)
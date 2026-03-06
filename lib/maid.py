import os
import sys

def cleanup():
    print("cleaning up")
    os.remove("config.json")
    s = os.path.exists("config.json")

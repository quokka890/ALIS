import os

def cleanup():
    print("cleaning up")
    os.remove("config.json")
    s = os.path.exists("config.json")

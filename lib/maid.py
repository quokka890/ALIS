import os
import sys

print("Current Working Directory:", os.getcwd())
print("\nPython Search Paths:")
for path in sys.path:
    print(path)

def cleanup():
    print("cleaning up")
    os.remove("config.json")
    s = os.path.exists("config.json")

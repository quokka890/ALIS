import json
from lib.config_manager import genereate_config
import lib.utils.checks
from lib.utils.checks import prelim_checks  
from lib.utils.disk_utils import get_diskpath
from lib.syscommands import run_command

genereate_config()

with open("config.json") as config:
    config = json.load(config)
    print(config)
diskpath = get_diskpath(config["disk"])
### PREPARE DISK ###
print("starting disk partitioning")
run_command('dd if=/dev/urandom of="'+diskpath+'" BS=64M status=progress')
print("Disk preparation successful. Formatting...")
run_command('parted "'+diskpath+'" --script mklabel gpt mkpart primary 1MiB 4097MiB mkpart primary 4097MiB 36865MiB')
run_command('parted "'+diskpath+'" --script print ')

print('"'+diskpath+'" earm')
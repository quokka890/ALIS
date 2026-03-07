import json
from lib.config_manager import genereate_config
import lib.utils.checks
from lib.utils.checks import prelim_checks  
from lib.utils.disk_utils import get_disk_info
from lib.syscommands import run_command

journal = lib.journal

with open("config.json") as config:
    config = json.load(config)

diskpath = get_disk_info(config["disk"])
p1 = get_disk_info(config["disk", 1])
p2 = get_disk_info(config["disk", 2])
p3 = get_disk_info(config["disk", 3])

genereate_config()
def partition():
    ### PREPARE DISK ###
    with journal.load: 
        run_command(f'dd if=/dev/urandom of={diskpath} BS=64M status=progress')
    print("Disk preparation successful. Formatting...")
    run_command(f'parted {diskpath} --script mklabel gpt mkpart primary 1MiB 4097MiB mkpart primary 4097MiB 36865MiB')
    run_command(f'parted {diskpath} --script print ')
    print("Disk formatting successful")

def encrypt():
    if config["encrypt"] == True: 
        run_command(f'cryptsetup luksFormat {p1}')
        run_command(f'cryptseup open {p1} cryptlvm')
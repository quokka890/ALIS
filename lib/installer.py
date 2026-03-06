import json
import lib.config_manager
import lib.utils.checks
from lib.utils.checks import prelim_checks
from lib.utils.disk_utils import get_diskpath
from lib.syscommands import run_command

prelim_checks()
config = json.load('config.json')
diskpath = get_diskpath(config["disk"])

def prep_disk():
    if input("Starting disk preparation. THIS WILL ERASE ALL DATA ON ", config["disk"], ". Are you sure you want to proceed? y/N") != "y":
        exit(0)
    run_command("dd if=/dev/urandom of=", diskpath, " BS=64M status=progress")
    print("Disk preparation successful. Formatting...")
    run_command("parted ", diskpath, "--script mklabel gpt mkpart P1 ", config["filesystem"], "2048MiB")
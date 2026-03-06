from lib.syscommands import run_command
import inspect
def get_disks():
    run_command("lsblk -dno NAME")

get_disks()
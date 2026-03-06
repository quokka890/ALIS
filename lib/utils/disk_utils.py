from lib.syscommands import run_command
import inspect

def get_disks():
    disk_list = run_command("lsblk -dno NAME,SIZE", True)
    return disk_list

def get_diskpath(disk):
    return (f'/dev/{disk}')
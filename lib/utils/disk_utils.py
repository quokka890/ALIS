from lib.syscommands import run_command
import inspect

def get_disk_info():
    disk_list_info = run_command("lsblk -dno NAME,SIZE", True)
    return disk_list_info

def get_disks():
    disk_list = run_command("lsblk -dno NAME", True)
    return disk_list

def get_diskpath(disk):
    return ("/dev/", disk)
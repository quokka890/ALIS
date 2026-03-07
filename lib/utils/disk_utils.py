from lib.syscommands import run_command
import inspect

def get_disks():
    disk_list = run_command("lsblk -dno NAME,SIZE", True)
    return disk_list

def get_disk_info(disk, PartitionNumber="foo"):
    if partition != None and "nvme" in disk:
        return(f'/dev/{disk}', f'/dev/{disk}p{PartitionNumber}')
    else:
        return(f'/dev/{disk}', f'/dev/{disk}{PartitionNumber}')
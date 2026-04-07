from syscommands import cmd
import inspect
import journal
def get_disks():
    disk_list = cmd("lsblk -dno NAME,SIZE", True)
    return disk_list

def get_disk_info(disk, PartitionNumber=None):
    if PartitionNumber is not None and "nvme" in disk:
        return(f'/dev/{disk}p{PartitionNumber}')
    elif PartitionNumber is not None:
        return(f'/dev/{disk}{PartitionNumber}')
    else: 
        return (f'/dev/{disk}')

def get_uuid(partition):
    uuid = cmd(f'blkid -s UUID -o value {partition}')
    if not uuid:
        journal.fatal(f'Could not get UUID for {partition}')
    return uuid
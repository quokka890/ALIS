import configparser
import inquirer 
from utils.disk_utils import get_disks

get_disks()

questions = [
    inquirer.List("disk",
        
    )
]

def get_user_inputs(disk, encrypt):
    disk = input("Enter disk name (e.g /dev/nvme0n1):")

    encrypt = input("Encrypt the system? (Y/n):")
    if not encrypt:
        return True
    else: return False
    
    filesystem = input("")
def create_config():
    config = configparser.ConfigParser()

    config['Disk'] = {
        'disk': disk,
        'encryption': encrypt,
        'filesystem': "s"
    }

    config['Localization'] = {
        'name': 'louis',
        'locale-gen': 'en_US.UTF-8 UTF-8',
        'locale-conf': 'LANG=en_US.UTF-8',
    }

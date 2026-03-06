import configparser
import inquirer 
import json
import os
from types import SimpleNamespace
from lib.utils.disk_utils import get_disks

disk_list = get_disks()

questions = [
    inquirer.List("disk",
        message="Select disk:",
        choices=disk_list
    ),
    inquirer.List("filesystem",
        message="Select which filesystem to use:",
        choices=['ext4', 'btrfs']
    ),
    inquirer.Confirm("encrypt",
        message="Encrypt the filesystem?",
        default=True
    ),
    inquirer.Text("root_password",
        message="Enter root password"
    ),
    inquirer.Confirm("reuse_passwd_bool",
        message="Reuse root password for user?",
        default=True
    ),
]

def genereate_config():
    if os.path.exists("config.json"):
        print("it exists")
        return 0
    config = inquirer.prompt(questions)
    json_str = json.dumps(config).strip()
    with open("config.json", "w") as f: 
        f.write(json_str)
genereate_config()
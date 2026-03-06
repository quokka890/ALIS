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
    config = inquirer.prompt(questions)
    config = format(config["disk"]).strip("1234567890,GT ")
    json_str = json.dumps(config).strip()
    #check if file exists. if it does then overwrite, else create 
    if os.path.exists("config.json"):
        with open("config.json", "w") as f:
            f.write(json_str)
        return 0
    else:
        with open("config.json", "w") as f: 
            f.write(json_str)
import configparser
import inquirer 
import json
import os
from types import SimpleNamespace
from utils.disk_utils import get_disks 

global config

disk_list = get_disks()

questions = [
    inquirer.List(
        "disk",
        message="Select disk:",
        choices=disk_list
    ),
    inquirer.Text(
        "encryption_password",
        message="Enter encryption password:"
    ),
    inquirer.Text(
        "root_password",
        message="Enter root password:",
    ),
    inquirer.Text(
        "user_name",    
        message="Enter your user name:",
    ),
    inquirer.Text(
        "user_password",
        message="Enter your user password:"
    )
]

advanced_questions = [
    inquirer.Checkbox(
        'reducepartsize',
        message="Use reduced partition sizes?",
        choices=['Yes (>32GB)', 'No'],
    )
]

def generate_config(advanced_mode=False):
    if advanced_mode == True:
        config = inquirer.prompt(questions + advanced_questions)
    else:
        config = inquirer.prompt(questions)
    config["disk"]=format(config["disk"]).strip("1234567890,.GTMIB ")
    json_str = json.dumps(config).strip()
    #check if file exists. if it does then overwrite, else create 

    with open("config.json", "w") as f:
        f.write(json_str)


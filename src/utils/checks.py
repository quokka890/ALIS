import journal
import json
from syscommands import cmd

with open("config.json", "r") as config:
    config = json.load(config)

def run_checks():
    if config["encryption_password"] == config["root_password"]:
        journal.warn("SECURITY WARNING: Your encryption password and root password are the same")
    if config["root_password"] == config["user_password"]:
        journal.warn("SECURITY WARNING: The root password and user password are the same")
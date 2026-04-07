import os
import json
import shutil
import journal
from syscommands import cmd_safemode

def _base_cleanup():
    #remove cache and other leftover python files
    for path in ['__pycache__', 'src/__pycache__', 'utils/__pycache__']:
        if os.path.exists(path):
            shutil.rmtree(path)
    for path in os.listdir('.'):
        if path.endswith('.egg-info'):
            shutil.rmtree(path)
    if os.path.exists("config.json"):
        global config
        with open("config.json", "r") as f:
            config = json.load(f)
        journal.section("DEBUG: CONFIG TABLE")
        journal.info(config, omit=True)
        os.remove("config.json")
    cmd_safemode('umount /mnt/efi')
    cmd_safemode('umount -R /mnt')
    cmd_safemode('swapoff -a')



def cleanup_error(error):
    _base_cleanup()
    cmd_safemode('vgchange -an SystemVolumeGroup')
    cmd_safemode('cryptsetup close cryptlvm')
    cmd_safemode(f'blockdev --rereadpt {config["disk"]}') 
    cmd_safemode('udevadm settle')

def cleanup_success(ExitCode=1, debug=False):
    _base_cleanup()
    if debug == True:
        journal.debug('Exiting without cleaning up due to debug mode')
        return
    journal.success("Installation successful. Reboot from the new system to continue.")
    


        
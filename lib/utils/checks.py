from lib.syscommands import run_command
# check if NOT on archiso
host = run_command("echo $HOST")
# check if root
uid = run_command("id -u") 
if uid != 0 and host=="archiso": # if not root and on archiso then exit
    print("Failed safety check (REQUIRED RUNNING AS ROOT)")
    exit(1)
if uid == 0 and host != "archiso": # if root and not on archiso then exit
    print("Failed safety check (RUNNING ON ROOT OUTSIDE OF ARCHISO IS DISABLED)")
    exit (1)

def prelim_checks():
    # Preliminary checks before proceeding with installation
    # UEFI bitness
    bitness = run_command("cat /sys/firmware/efi/fw_platform_size")
    if bitness != "64":
        print("Prelim checks failed: not running in 64-bit UEFI mode")
        exit(1)
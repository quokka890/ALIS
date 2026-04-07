import subprocess
import journal

class InstallError(Exception):
    def __init__(self, message, command=None, returncode=None):
        super().__init__(message)
        self.command = command
        self.returncode = returncode

def cmd(command, output_list=False):
    
    result = subprocess.run(
        command, 
        text=True, 
        capture_output=True, 
        shell=True
    )

    if result.returncode != 0:
        err_msg = (
            f"COMMAND FAILED: {command}"
            f"{'ERROR:'} {result.stderr}"
            f"{'RET CODE:'} {result.returncode}"
        )
        journal.info("Exiting with exit code 1")
        journal.fatal(err_msg)
        raise InstallError(message = "Command failed", command=command, returncode=result.returncode)
        
    # log success
    output = result.stdout.strip()
    journal.log_command(f'SUCCESS: "{command}" | OUTPUT: "{output}..."')

    if output_list:
        return result.stdout.splitlines()
    
    return output

def cmd_safemode(command):
    result = subprocess.run(
    command, 
    text=True, 
    capture_output=True, 
    shell=True
    )
    return result


def chroot(command, target="/mnt"):
    chroot_command = f'arch-chroot {target} {command}'
    return cmd(chroot_command)
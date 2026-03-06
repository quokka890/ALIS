import subprocess

def run_command(command, Convert_Output_To_List=False):
    import lib.utils.checks
    raw_output = subprocess.run(command, shell = True, text = True, capture_output= True, executable="/bin/bash")

    if Convert_Output_To_List == True:
        output_list = raw_output.stdout.splitlines()
        return output_list
    else:
        output = raw_output.stdout.strip()
        return output

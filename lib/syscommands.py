import subprocess
import journal

def run_command(command, Convert_Output_To_List=False):
    import lib.utils.checks
    raw_output = subprocess.run(command, shell = True, text = True, capture_output= True, executable="/bin/bash")
    print("raw output: ", raw_output)
    
    if raw_output.check_returncode !=0:
        log=f'FATAL: failed to execute command "{command}" with error "{raw_output.stderr}" and return code "{raw_output.returncode}"'
        journal.fatal(log)

    if Convert_Output_To_List == True:
        output_list = raw_output.stdout.splitlines()
        journal.log_command(output_list)
        return output_list
    else:
        output = raw_output.stdout.strip()
        journal.log_command(output)
        print("processed output: ", output)
        return output

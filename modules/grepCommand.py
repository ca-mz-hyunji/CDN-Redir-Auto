import subprocess
from .helpers import log

def grepCommand(path_from, logging_file_path):
    log("Finding Redirection Log Files \n", logging_file_path)

    ### For SSH ###
    log_files = subprocess.check_output(['grep', '-rl', path_from, '/m2log'], universal_newlines=True)
    log_files_list = log_files.strip().split('\n')
    log_files_list_sorted = sorted(log_files_list, key=len)

    # Remove origins
    for log_file in log_files_list_sorted:
        if log_file.find('origin') != -1:
            log_files_list_sorted.remove(log_file)
    
    # Print sorted log file lists (if not Excel mode)
    count = 1
    for log_file in log_files_list_sorted:
        log(f"Log file {count}: [{log_file}]", logging_file_path)
        count += 1
    
    log("", logging_file_path)

    return log_files_list_sorted
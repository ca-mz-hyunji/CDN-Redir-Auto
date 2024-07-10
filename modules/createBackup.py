import os
import json

from .helpers import dateTitle, log

def createBackup(json_path, logging_file_path):
    if not os.path.exists(json_path):
        log(f"JSON file '{json_path}' not found.", logging_file_path)
        return
   
    json_name = json_path.split("/")[-1]
    file_name = dateTitle(json_name)

    curr_path = str(os.getcwd())
    # Might need to change depending on the current path
    file_path = os.path.join(curr_path, "backups", file_name)

    with open(json_path, "r") as origin:
        data = json.load(origin)
    with open(file_path, "w") as copy:
        json.dump(data, copy, indent=3)
   
    print(f"Backup file {file_name} created in '{file_path}'\n")
    log(f"Backup file {file_name} created in '{file_path}'\n", logging_file_path)

    return 0
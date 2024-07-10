import time
import sys
import shutil
from .curlCommand import curlCommand
from .helpers import log

def testRedirection(domain, ip, path_from, dst_url, action, logging_file_path):

    max_attempts = 5
    success = False

    for attempt in range(1, max_attempts + 1):
        print(f"Attempt {attempt}/{max_attempts}")

        loc_eq_dst, location = curlCommand(domain, ip, path_from, dst_url, logging_file_path)

        if loc_eq_dst == True:
            if action == 'add' or action == 'modify':
                success = True
        else:
            if action == 'delete':
                success = True

        if success == True:
            log(f"{action}ing Redirection Rule has Sucessfully been Tested!", logging_file_path)
            log(f"Now redirected to {location}")
            return success

        if attempt < max_attempts:
            log("Waiting 10 seconds before attempting curl command again\n", logging_file_path)
            time.sleep(10)

    return success
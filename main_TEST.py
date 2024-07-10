import os

from modules.helpers import border_msg, userData
from modules.userInput import userInput
from modules.curlCommand import curlCommand
from modules.checkAction import checkAction
from modules.grepCommand import grepCommand
from modules.findVirtualHostname import findVirtualHostname
from modules.findBaseHost import findBaseHost
from modules.openConfigFile import openConfigFile
from modules.logRedirRules import logRedirRules
from modules.createBackup import createBackup
from modules.updateFile import updateFile
from modules.m2DeployLocal import m2DeployLocal
from modules.testRedirection import testRedirection
from modules.helpers import userData, border_msg, log

def main():
    ### Phase 1 ###
    domain_failed = {}
    check_action_failed = {}
    check_config_failed = {}
    config_file_list = []
    check_testRedirection_failed = {}

    # Step 1: Get inputs from User
    excel_file_path = input("Type in the CSV file path: ")
    # /Users/hyunjikim/Desktop/GitHub/CDN-final/test.csv
    if not os.path.exists(excel_file_path):
        border_msg(f"CSV file '{excel_file_path}' not found.")
        return
    
    # Used to make detailed logs in a Log File and simplify the Terminal output
    curr_path = str(os.getcwd())
    logging_file = input("Enter the Ticket Number to create a Log File: ")
    logging_file_path = os.path.join(curr_path, "log_files", logging_file)
    ### for testing
    print(logging_file_path)

    user_input_dict = userInput(excel_file_path)
    # user_input_dict = {{'src_url', 'domain', 'ip', 'path_from', 'dst_url', 'action'}}
    ### for testing
    for i in user_input_dict:
        print(user_input_dict[i])

    for user_input in user_input_dict:
        # Retrieve variables from User Input CSV file
        src_url, domain, ip, path_from, dst_url, action = userData(user_input_dict[user_input])        
        log(f"Index [{user_input+1}]", logging_file_path)
        log(f"Source URL: [{src_url}]", logging_file_path)
        log(f"Destination URL: [{dst_url}]", logging_file_path)
        log(f"Action: [{action}]", logging_file_path)

        if domain == None:
            domain_failed[user_input] = user_input_dict[user_input]
            log('Domain of Source URL is Invalid', logging_file_path)
            continue
        
        # Step 2: Send Curl (check Destination & make a log if there wasn't)
        loc_eq_dst, location = curlCommand(domain, ip, path_from, dst_url, logging_file_path)

    return 0

if __name__=='__main__':
    main()
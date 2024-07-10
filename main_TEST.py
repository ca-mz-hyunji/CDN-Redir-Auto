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
    logging_file_path = os.path.join(curr_path, "log_files", logging_file+".log")

    user_input_dict = userInput(excel_file_path)
    # user_input_dict = {{'src_url', 'domain', 'ip', 'path_from', 'dst_url', 'action'}}

    for user_input in user_input_dict:
        # Retrieve variables from User Input CSV file
        src_url, domain, ip, path_from, dst_url, action = userData(user_input_dict[user_input])
        log('----------------------------------------', logging_file_path)        
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

        # Step 3: Check the 8 cases (Add, Modify, Delete)
        new_action = checkAction(src_url, loc_eq_dst, location, action, logging_file_path)
        
        if action != new_action:    # if new_action is different from the initial action or False
            if new_action == False:
                check_action_failed[user_input] = user_input_dict[user_input]
                continue
            else:
                user_input_dict[user_input]['action'] = new_action
    
        # If "www.hyundai.com", Skip Steps 4,5,6 as base hosts are given
        if domain == "www.hyundai.com":
            base_hosts = {"basehost1": "/usr/local/m2/json/www.hyundai.com/www.hyundai.com.json", "basehost2": "/usr/local/m2/json/www.hyundai.com/www.hyundai.com-default.json"}
        else:
            log_files = grepCommand(path_from, logging_file_path)
            virt_hosts = findVirtualHostname(log_files, path_from, logging_file_path)
            base_hosts = findBaseHost(virt_hosts, logging_file_path)   # dictionary
                                                                       # NEED TO CHANGE??? - 왜
        
        config_pattern, config_location, config_file_loc, config_checked = openConfigFile(base_hosts, path_from, src_url, dst_url, new_action, logging_file_path)
        if config_checked == False:
            check_config_failed[user_input] = user_input_dict[user_input]
            continue

        #logRedirRules(config_pattern, config_location, action, path_from, dst_url, logging_file_path)

        # Note: Create backup only when it is the first redirection rule (no need to create multiple backup files) --> IN PROCESS
        if config_file_loc not in config_file_list:
            config_file_list.append(config_file_loc)
            createBackup(config_file_loc, logging_file_path)

        updateFile(path_from, dst_url, new_action, config_file_loc, logging_file_path)

    ### for testing
    print("------------")
    if domain_failed:
        for domain_failed_index in domain_failed:
            print(f"ERROR: Index {domain_failed_index+1}: [{domain_failed[domain_failed_index]['src_url']}] does not have a valid domain name. Try it again later.")
    else:
        print("ALL domains were valid")
    print("------------")
    if check_action_failed:
        for action_failed_index in check_action_failed:
            print(f"ERROR: Index [{action_failed_index+1}] failed to check action. src_url: [{check_action_failed[action_failed_index]['src_url']}] & dst_url: [{check_action_failed[action_failed_index]['dst_url']}]")
    else:
        print("ALL actions were valid")
    print("------------")
    if check_config_failed:
        for config_failed_index in check_config_failed:
            print(f"ERROR: Index [{config_failed_index+1}] with src_url: [{check_config_failed[config_failed_index]['src_url']}] could not find the rule in any configuration file")
    else:
        print("ALL config files were valid")
    print("------------")

if __name__=='__main__':
    main()
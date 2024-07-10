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
    check_update_failed = {}
    check_testRedirection_failed = {}

    # Step 1: Get inputs from User
    excel_file_path = input("Type in the CSV file path: ")
    if not os.path.exists(excel_file_path):
        border_msg(f"CSV file '{excel_file_path}' not found.")
        return
         
    # Used to make detailed logs in a Log File and simplify the Terminal output
    curr_path = str(os.getcwd())
    logging_file = input("Enter the Ticket Number to create a Log File: ")
    logging_file_path = os.path.join(curr_path, "log_files", logging_file)

    user_input_dict = userInput(excel_file_path)
    # user_input_dict = {{'src_url', 'domain', 'ip', 'path_from', 'dst_url', 'action'}}

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
            # Step 4: Grep Command --> Find Log Files (sort into shortest first)
            log_files = grepCommand(path_from, logging_file_path) 
                
            # Step 5: Open the (shortest) log file (don't use /origin.log) and find Virtual Hostname for Path_from
            virt_hosts = findVirtualHostname(log_files, path_from, logging_file_path)
                
            # Step 6: Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
            base_hosts = findBaseHost(virt_hosts, logging_file_path)   # dictionary
            ################## NEED TO CHANGE !!!! because bast_hosts is for THIS user_input and Step 12 will be use the last user_input base_hosts ###########################
            
        # Step 7: Open the JSON config file (located at BaseHost) and search for redirection rule (using Path_from)
        config_pattern, config_location, config_file_loc, config_checked = openConfigFile(base_hosts, path_from, src_url, dst_url, action, logging_file_path)

        if config_checked == False:
            check_config_failed[user_input] = user_input_dict[user_input]
            continue

        ### Phase 2 ###
        # Step 8: Log the redirection rule (pattern) to Add/Modify/Delete
        logRedirRules(config_pattern, config_location, action, path_from, dst_url, logging_file_path)

        # FOR TESTING: remove the line if you want to edit the real configuration file
        config_file_loc = "/home/hji_kim/automation/www.kia.com-acl-testing.json"

        # Step 9: Copy a backup file in a subdirectory
        # Note: Create backup only when it is the first redirection rule (no need to create multiple backup files) --> IN PROCESS
        if config_file_loc not in config_file_list:
            config_file_list.append(config_file_loc)
            createBackup(config_file_loc, logging_file_path)

        # Step 10: Update the Config File with redirection rule
        updateFile(path_from, dst_url, action, config_file_loc, logging_file_path)

    # Step 11: Deploy
    m2DeployLocal(logging_file_path)

    # Step 12: Test the redirection change by using Curl (every 2 minutes, 5 times max)
    print("Testing all Redirection Rule changes applied... Please Wait...")
    for user_input in user_input_dict:
        if user_input in domain_failed or check_action_failed or check_config_failed or check_testRedirection_failed:
            continue
        src_url, domain, ip, path_from, dst_url, action = userData(user_input_dict[user_input])
        success = testRedirection(domain, ip, path_from, dst_url, action, logging_file_path)
        if success == False:
            check_testRedirection_failed[user_input] = user_input_dict[user_input]


    print("------------")
    for domain_failed_index in domain_failed:
        print(f"ERROR: Index {domain_failed_index+1}: [{domain_failed[domain_failed_index]['src_url']}] does not have a valid domain name. Try it again later.")
    print("------------")
    for action_failed_index in check_action_failed:
        print(f"ERROR: Index [{action_failed_index+1}] failed to check action. src_url: [{check_action_failed[action_failed_index]['src_url']}] & dst_url: [{check_action_failed[action_failed_index]['dst_url']}]")
    print("------------")
    for config_failed_index in check_config_failed:
        print(f"ERROR: Index [{config_failed_index+1}] with src_url: [{check_config_failed[config_failed_index]['src_url']}] could not find the rule in any configuration file")
    print("------------")
    for check_testRedirection_failed_index in check_testRedirection_failed:
        print(f"ERROR: Index [{check_testRedirection_failed_index+1}] with src_url: [{check_testRedirection_failed[check_testRedirection_failed_index]['src_url']}] failed Redirection Test")
    print("------------")

if __name__=='__main__':
    main()
    # /home/hji_kim/automation/kia_test.csv
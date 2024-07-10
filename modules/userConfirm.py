import json
import sys

def userConfirm(config_pattern, config_location, action, path_from, dst_url):
    
    rule = {
        "pattern": config_pattern,
        "action": "redirect",
        "location": config_location,
        "denialCode": 301
    }

    rule_add = {
        "pattern":  f"$URL[{path_from}]",
        "action": "redirect",
        "location": dst_url,
        "denialCode": 301
    }

    if action == "add":
        print("rule = " + json.dumps(rule_add, indent=4) + "\n")
        confirmed = input("Confirmation: Would you like to ADD the following redirection rule? (yes/no): ").lower()
        while confirmed not in ('yes','no'):
            confirmed = input("Confirmation: Would you like to ADD the following redirection rule? (yes/no): ").lower()
    
    elif action == "modify":
        print("rule = " + json.dumps(rule, indent=4) + "\n")
        confirmed = input("Confirmation: Would you like to MODIFY the following redirection rule? (yes/no): ").lower()
        while confirmed not in ('yes','no'):
            confirmed = input("Confirmation: Would you like to MODIFY the following redirection rule? (yes/no): ").lower()
        
    elif action == "delete":
        print("rule = " + json.dumps(rule, indent=4) + "\n")
        confirmed = input("Confirmation: Would you like to DELETE the following redirection rule? (yes/no): ").lower()
        while confirmed not in ('yes','no'):
            confirmed = input("Confirmation: Would you like to DELETE the following redirection rule? (yes/no): ").lower()

    if confirmed == 'no':
        print("\nExiting Code\n")
        sys.exit("User did not confirm to proceed with the Redirection Automation process.")
    else:
        print("\nConfirmed to Redirect\n")


    return confirmed, rule_add if action == 'add' else rule

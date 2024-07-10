import json
import os
from .helpers import log

def updateFile(path_from, dst_url, action, config_file_loc, logging_file_path):
    index = 0

    if not os.path.exists(config_file_loc):
        log(f"JSON file '{config_file_loc}' not found.", logging_file_path)
        return
    
    with open(config_file_loc, 'r') as file:
        data = json.load(file)
        rules = data["functions"]["network"]["http"]["frontEnd"]["accessControl"]["matchingList"]
        if action == 'add':
            rule_add = {
                        "pattern":  f"$URL[{path_from}]",
                        "action": "redirect",
                        "location": dst_url,
                        "denialCode": 301
                        }
            # print(f"Rule {rule_add} ADDED.")
            log("Rule:\n" + json.dumps(rule_add, indent=4) + "\nADDED", logging_file_path)
            rules.append(rule_add)
        else:
            for rule in rules:
                if rule["pattern"] == f"$URL[{path_from}]":
                    if action == 'modify':
                        rule["location"] = dst_url
                        # print(f"Rule {rule} MODIFIED.")
                        log("Rule:\n" + json.dumps(rule, indent=4) + "\nMODIFIED", logging_file_path)
                        break
                    else:
                        if rule["location"] == dst_url:
                            # print(f"Rule {rule} DELETED.")
                            log("Rule:\n" + json.dumps(rule, indent=4) + "\nDELETED", logging_file_path)
                            del rules[index]
                            break
                index += 1
    
    with open(config_file_loc, 'w') as file:
        json.dump(data, file, indent=2)
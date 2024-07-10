import json
from .helpers import log


def logRedirRules(config_pattern, config_location, action, path_from, dst_url, logging_file_path):
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
        log("rule = " + json.dumps(rule_add, indent=4) + "\n" + "ADDED\n", logging_file_path)
    elif action == "modify":
        log("rule = " + json.dumps(rule, indent=4) + "\n" + "MODIFIED To: \n", logging_file_path)
        log("rule = " + json.dumps(rule_add, indent=4), logging_file_path)
    else:
        log("rule = " + json.dumps(rule, indent=4) + "\n" + "DELETED\n", logging_file_path)

    return 0
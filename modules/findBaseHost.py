import os
import json

from .helpers import removeDuplicates, log

# Step 6: Find BaseHost for the Virtual Hostname (from /usr/local/m2/setting.json)
def findBaseHost(virt_hosts, logging_file_path):
    # virt_hosts == list
    base_hosts = {}
    for virt_host in virt_hosts:
        base_hosts.setdefault(virt_host)

    json_file = "/usr/local/m2/setting.json"

    if not os.path.exists(json_file):
        log(f"JSON file '{json_file}' not found.", logging_file_path)

    with open(json_file, 'r') as file:
        data = json.load(file)
        hosting = data["hosting"]

        for item in hosting:
            if item["name"] in virt_hosts:
                base_hosts[item["name"]] = item["mode"]["basehost"]

    # Remove duplicates
    new_base_hosts = removeDuplicates(base_hosts)

    # Print sorted base hosts lists
    count = 1
    for base_host in new_base_hosts:
        log(f"Base Host {count}: [{new_base_hosts[base_host].split('/')[-1]}]", logging_file_path)
        count += 1
    log("", logging_file_path)

    return new_base_hosts
import subprocess
import re
from .helpers import log

# Step 2: Send Curl (check Destination & make a log if there wasn't)
def curlCommand(domain, ip, path_from, dst_url, logging_file_path):

    curl_command = f'curl -I -H "HOST:{domain}" http://{ip}{path_from}'
    curl_output = subprocess.run(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    
    log("Checking Redirection... \n", logging_file_path)
    log(f'Running: {curl_command}\n', logging_file_path)

    if curl_output.returncode == 0:
        log(f"Curl Command succeeded. \n", logging_file_path)
        log(f"Output:\n{curl_output.stdout}", logging_file_path)
    else:
        log("Curl Command failed with Error: \n", logging_file_path)
        log(curl_output.stderr, logging_file_path)

    # To Find the HTTP Protocol
    status_pattern = re.compile(r"HTTP/.*")
    # To Find the Redirection URL Location
    location_line = None
    loc_pattern = re.compile(r"location: .*")

    all_lines = curl_output.stdout.splitlines()

    for line in all_lines:
        if status_pattern.match(line):
            status_line = line

        if loc_pattern.match(line):
            location_line = line
            break
    
    status = status_line.split(" ")[1]

    if status == "404":
        location = None
    else:
        location = location_line.split(" ")[1]
        log("Currently Redirected to: [" + location + "]\n", logging_file_path)
    
    log("HTTP Status: [" + status_line + "]\n", logging_file_path)

    loc_eq_dst = False

    # If Redirection URL Location is same as dst_url
    if location == dst_url:
        loc_eq_dst = True
    
    return loc_eq_dst, location
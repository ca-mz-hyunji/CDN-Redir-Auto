from .helpers import readUntilMatch, log

def findVirtualHostname(log_files, path_from, logging_file_path):
    virt_hosts = []

    for log_file in log_files:
        match_line = readUntilMatch(log_file, path_from)

        if match_line:
            try:
                id_marker = "id=- "
                http_marker = "HTTP"

                start_index = match_line.index(id_marker) + len(id_marker)
                end_index = match_line.index(http_marker, start_index)

                substring = match_line[start_index:end_index].strip()

                # Edge case where the substring looks like this: 
                # "id=- - multimedia.html www.hyundai.com-eu-80 HTTP"
                # Split the substring by spaces and find the Virtual Hostname that contains "www."
                items = substring.split()
                virt_host = next((item for item in items if "www." in item), None)

            except ValueError:
                virt_host = None
        else:
            virt_host = None

        if virt_host not in virt_hosts:
            virt_hosts.append(virt_host)

    virt_hosts_filter = list(filter(lambda item: item is not None, virt_hosts))
    virt_hosts_sorted = sorted(virt_hosts_filter, key=len)

    # Print sorted virtual host names (if not Excel mode)
    count = 1
    for virt_host in virt_hosts_sorted:
        log(f"Virtual Hostname {count}: [{virt_host}]", logging_file_path)
        count += 1
    log("", logging_file_path)

    return virt_hosts_sorted
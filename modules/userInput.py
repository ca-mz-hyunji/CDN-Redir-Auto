import csv
from .helpers import splitURL, IP_dict, border_msg

def userInput(excel_file_path):
    user_input_dict = {}
    # domain_failed = {}

    src_urls = []
    dst_urls = []
    actions = []
    
    with open(excel_file_path, mode='r') as file:
        lines = csv.reader(file)
        # skip header
        next(lines)
    
        # Assumme the first row is the header
        # Assume the first (A) column is the source URL
        # Assume the second (B) column is the Redirection code
        # Assume the third (C) column is the destination URL

        for line in lines:
            src_urls.append(line[0])
            dst_urls.append(line[1])
            actions.append(line[2])

    index = 0
    while index < len(src_urls):
        domain, path_from = splitURL(src_urls[index])
        if domain not in IP_dict:
            domain = None
            ip = None
        else:
            ip = IP_dict[domain]
        
        user_input_dict[index] = {'src_url': src_urls[index],
                                    'domain': domain,
                                    'ip': ip,
                                    'path_from': path_from,
                                    'dst_url': dst_urls[index],
                                    'action': actions[index]}
        index += 1

    return user_input_dict
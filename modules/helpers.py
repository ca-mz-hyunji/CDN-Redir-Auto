# Folder
import datetime

IP_dict = {
    "www.kia.com": "34.160.76.133",
    "www.hyundai.com": "192.168.10.43",
    "www.hyundaiusa.com": "34.160.79.194",
    "www.genesis.com": "192.168.10.44",
    "www.casper.hyundai.com": "35.244.253.146",
    "casper.hyundai.com": "34.64.165.126 ",
    "sweb.hyundaiusa.com": "34.149.243.31",
    "sweb-owners.genesis.com": "34.117.224.125",
    "owners.genesis.com": "34.36.215.56",
    "owners-kia.com": "34.110.185.95",
    "preprod2-eu.kia.com": "34.102.172.183",
    "connectstore.kia.com": "34.49.88.90"
}

def splitURL(url):
    # url = https://www.kia.com/hello/world/
    try:
        # url = url.lower()
        domain_path = url.split("://")[1] # domain_path = 'www.kia.com/hello/world/'
        domain = domain_path.split("/")[0] # domain = 'www.kia.com'
        path_from = domain_path.replace(domain, '') # path_from = '/hello/world/'
        return domain, path_from
    except Exception:
        return None, None
    

def readUntilMatch(file, search_string):
    with open(file, 'r') as f:
        # Read all lines from the file
        lines = f.readlines()
    
    # Reverse the list of lines to start from the bottom
    lines.reverse()

    # Iterate through the reversed lines
    for line in lines:
        if search_string in line: # If path_from found in line
            return line # Return the first matching line from bottom 
    return None  # Return None if no match is found

def removeDuplicates(dict):
    temp = []
    res = {}

    for key in dict:
        if dict[key] not in temp:
            temp.append(dict[key])
            res[key]=dict[key]

    return res

def dateTitle(json_file_name):
   date = datetime.datetime.now()
   date = str(date).replace(" ", "-")
   date = date.split(".")[0]
   date = date.replace(":", "-")
   name = str(json_file_name).replace(".json", "")
   file_name = f"{name}-{date}.json"

   return file_name

def userData(user_input):
    src_url = user_input['src_url']
    domain = user_input['domain']
    ip = user_input['ip']
    path_from = user_input['path_from']
    dst_url = user_input['dst_url']
    action = user_input['action']

    return src_url, domain, ip, path_from, dst_url, action

# Source: https://stackoverflow.com/questions/39969064/how-to-print-a-message-box-in-python
def border_msg(msg):
    row = len(msg)
    h = ''.join(['+'] + ['-' *row] + ['+'])
    result= h + '\n'"|"+msg+"|"'\n' + h
    print(result)

def log(txt, file_path):
    with open(file_path, "a") as f:
        f.write(txt + '\r\n')
import os
import json
import datetime

def dateTitle():
   date = datetime.datetime.now()
   date = str(date).replace(" ", "-")
   date = date.split(".")[0]
   return date

def createBackup(json_file):
   if not os.path.exists(json_file):
      print(f"JSON file '{json_file}' not found.")

   with open(json_file, 'r') as original:
      data = json.load(original)
      date = dateTitle()
      name = str(json_file).replace(".json", "")
      file_name = f"{name}-{date}.json"
      curr_path = str(os.getcwd())
      file_path = os.path.join(f"{curr_path}/backups", file_name)
      
   with open(file_path, 'w') as copy:
      json.dump(data, copy, indent=4)
      print(f"Backed up '{json_file}' in '{name}-{date}.json'")


if __name__=='__main__':
   createBackup("www.kia.com-acl.json")
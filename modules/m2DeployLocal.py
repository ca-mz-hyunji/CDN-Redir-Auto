import subprocess

from .helpers import log

def m2DeployLocal(logging_file_path):
    print("Sending command <m2 deploy local>\n")
    log("Sending command <m2 deploy local>\n", logging_file_path)

    deploy_result = subprocess.run("m2 deploy local", shell=True, capture_output=True, text=True)

    if deploy_result.returncode == 0:
        print(deploy_result.stdout)
        log(deploy_result.stdout, logging_file_path)
    else:
        print(deploy_result.stderr)
        log(deploy_result.stderr, logging_file_path)
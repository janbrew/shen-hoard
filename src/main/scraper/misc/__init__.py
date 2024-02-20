import os
from datetime import datetime

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
PATH = "{}\\download\\{}\\{}"

def init_download_dir(site):
    dir = PATH.format(os.getcwd(), site, datetime.strftime(datetime.today(), "%Y-%m-%d-%H-%M-%S"))

    if not os.path.exists(dir):
        os.makedirs(dir)

    return dir

def log(level, message):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    END = "\033[0m"
        
    if level == "INFO":
        print(GREEN + f"[{level}] : {message}" + END)
        
    elif level == "WARN":
        print(YELLOW + f"[{level}] : {message}" + END)

    elif level == "ERROR":
        print(RED + f"[{level}] : {message}" + END)

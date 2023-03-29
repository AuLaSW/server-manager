"""
server-manage.py
----------------

A python script for managing simple servers with shell-script calls.
"""
from utils import *


def main():
    server = BotFarm()
    
    server.load_servers()
    

if __name__ == "__main__":
    main()
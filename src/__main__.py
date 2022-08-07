#!/usr/bin/env python3

import json
import os
import sys

from __init__ import JSON_PATH
from auth import Authenticator
from help import Helper


def main():
    # Define the command line arguments.
    help_obj = Helper()
    if len(sys.argv) == 1:
        print("Writing help because there were no arguments.")
        help_obj.help_empty()
    elif len(sys.argv) == 2 and sys.argv[1].lower() == "help":
        print("Writing help since there is a single argument for help.")
        help_obj.help_empty()
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "login":
        print("Writing help login because it was requested.")
        help_obj.help_login()
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "logout":
        print("Writing help logout because it was requested.")
        help_obj.help_logout()
    elif len(sys.argv) >= 2 and sys.argv[1].lower() == "login":
        print("Attempting authentication.")
        auth_obj = Authenticator()
        auth_obj.supply_credentials(sys.argv[4], sys.argv[2], sys.argv[3])
        auth_obj.new_login()
    elif len(sys.argv) >= 2 and sys.argv[1].lower() == "logout":
        # Attempt to find the access token and instance.
        if os.path.isfile(JSON_PATH):
            current_config = dict()
            try:
                with open(JSON_PATH, "r") as config_file:
                    current_config = json.load(config_file)
            except Exception as e:
                print(f"ERROR: Unable to read {JSON_PATH} with error: {e}")

            if current_config != {} and current_config.get('instance') and current_config.get('access_token'):
                auth_obj = Authenticator()
                auth_obj.remove_login(
                    current_config.get('instance'),
                    current_config.get('access_token'))
        else:
            print(f"No config file found at: {JSON_PATH}")

    else:
        print("Something else was entered.")
        

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import json
import os
import sys

from __init__ import JSON_PATH
from auth import Authenticator
from config import ConfigObj
from help import Helper
from post import Post


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
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "post":
        post_content = ""
        if sys.argv[2] == "--":
            print("Reading post content from STDIN.")
            post_content = sys.stdin.read()
        else:
            if os.path.isfile(sys.argv[2]):
                with open(sys.argv[2], "r") as file:
                    post_content = file.read()
            else:
                print(f"Unable to find a file at given path of: {sys.argv[3]}")

        # Check if a collection was specified.
        collection = None
        if len(sys.argv) >= 4:
            collection = sys.argv[3]

        # Check if a title was specified.
        post_content_list = post_content.split('\n')
        post_title = None
        if post_content_list[0].startswith('#'):
            post_title = post_content_list[0].replace("#", "").strip()
            post_content_list.remove(post_content_list[0])
            post_content = '\n'.join(post_content_list)

        # Ensure we have information to connect to Write Freely.
        current_conf = ConfigObj()
        current_conf.load()

        # Create a post object and validate the collection if one was provided.
        current_post = Post(
            post_content,
            current_conf.instance,
            current_conf.access_token,
            collection=collection,
            title=post_title)

        if collection != "":
            current_post.check_collection()

        # Make the post.
        post_id = current_post.create_post()
        print(f"Successfully created post with ID: {post_id}")

    elif len(sys.argv) < 4 and "post" in sys.argv:
        print("Not enough arguments to make a post!")
        help_obj.help_post()
    else:
        print("Entered arguments don't match known values. Run \"writepyly help\" for instructions.")
        

if __name__ == "__main__":
    main()

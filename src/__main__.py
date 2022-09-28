#!/usr/bin/env python3

import json
import os
import sys

from rich.console import Console

from __init__ import JSON_PATH
from auth import Authenticator
from client import WriteFreely
from config import ConfigObj
from console import WriteConsole
from help import Helper
from post import Post

def exit_with_login_message(console: Console) -> None:
    """
    Prints a message that loading the configuration failed and prompting the user
    to run the login command.

    Args:
        console (Console): rich `Console` object for writing to stdout.
    """
    console.print("Running [bold purple]writepyly login[/bold purple] should resolve this.")
    sys.exit(1)

def string_to_int(input_value: str) -> int:
    """
    Attempts to convert a string to an integer and returns the integer value.

    Args:
        input_value (str): String to convert.

    Returns:
        int: The integer representation of the string.
    """
    try:
        return int(input_value)
    except ValueError:
        print("Must specify an integer for the page size! Run:")
        print("\n\t writepyly help get\n")
        print("For more details.")
        sys.exit(1)
    except Exception as e:
        print(f"Unknown error processing page size: {e}")
        sys.exit(1)

def main():
    # Create a console object.
    console = Console()

    # Define the command line arguments.
    help_obj = Helper()
    if len(sys.argv) == 1:
        # Launch the interactive TUI application.
        WriteConsole()
    elif len(sys.argv) == 2 and sys.argv[1].lower() == "help":
        help_obj.help_empty()
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "login":
        help_obj.help_login()
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "logout":
        help_obj.help_logout()
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "post":
        help_obj.help_post()
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "get":
        help_obj.help_get()
    elif len(sys.argv) >=3 and sys.argv[1].lower() == "help" and sys.argv[2].lower() == "delete":
        help_obj.help_delete()
    elif len(sys.argv) >= 2 and sys.argv[1].lower() == "login":
        if len(sys.argv) < 5:
            console.print("Not enough arguments! See the following for more details:\n\n[bold]writepyly help login[/bold]\n", style="red")
            sys.exit(1)
        console.print("Attempting authentication.")
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
                console.print(f"ERROR: Unable to read {JSON_PATH} with error: {e}", style="bold red")

            if current_config != {} and current_config.get('instance') and current_config.get('access_token'):
                auth_obj = Authenticator()
                try:
                    auth_obj.remove_login(
                        current_config['instance'],
                        current_config['access_token'])
                except KeyError as e:
                    console.print("Missing either the instance or access token to log out. Does the config file still exist at: ~/config/writepyly/config.json", style="bold red")
                    sys.exit(1)
                except Exception as e:
                    console.print(f"Failed to logout with error: {e}", style="bold red")
                    sys.exit(1)
        else:
            console.print(f"No config file found at: {JSON_PATH}")
    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "post":
        post_content = ""
        if sys.argv[2] == "--":
            console.print("Reading post content from STDIN.")
            post_content = sys.stdin.read()
        else:
            if os.path.isfile(sys.argv[2]):
                with open(sys.argv[2], "r") as file:
                    post_content = file.read()
            else:
                console.print(f"Unable to find a file at given path of: {sys.argv[3]}", style="bold red")
                sys.exit(1)

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
        if not current_conf.load():
            exit_with_login_message(console)

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
        console.print(f"Successfully created post with ID: [bold purple]{post_id}[/bold purple]")

    elif len(sys.argv) < 4 and "post" in sys.argv:
        console.print("Not enough arguments to make a post!", style="bold red")
        help_obj.help_post()
    elif len(sys.argv) >= 3 and "get" in sys.argv:
        # Load the configuration.
        current_config = ConfigObj()
        if not current_config.load():
            exit_with_login_message(console)

        # Create the client object and get the posts.
        write_client = WriteFreely(
            current_config.instance,
            current_config.access_token,
            collection=sys.argv[2])
        if not write_client.check_collection():
            sys.exit(1)
        write_client.get_posts()

    elif len(sys.argv) < 3 and "get" in sys.argv:
        console.print("Must specify a collection with [bold purple]get[/bold purple]. Please include the collection name.")
    elif len(sys.argv) >= 3 and "delete" in sys.argv:
        current_config = ConfigObj()
        if not current_config.load():
            exit_with_login_message(console)

        # Create the client and attempt to delete the post.
        write_client = WriteFreely(
            current_config.instance,
            current_config.access_token)
        write_client.delete_post(sys.argv[2])
    elif len(sys.argv) < 3 and "delete" in sys.argv:
        console.print("Must specify a post ID with 'delete'. Run [bold]\"writepyly help delete\"[/bold] for more details.", style="red")
    else:
        console.print("Entered arguments don't match known values. Run [bold]\"writepyly help\"[/bold] for instructions.", style="red")

if __name__ == "__main__":
    main()

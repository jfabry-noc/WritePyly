import getpass
import json
import os
import subprocess
import sys
import time
import uuid

from rich.console import Console

from auth import Authenticator
from config import ConfigObj
from client import WriteFreely
from post import Post

from __init__ import JSON_PATH, TEMP_BASE


class WriteConsole:
    # https://rich.readthedocs.io/en/latest/console.html
    def __init__(self):
        self.console = Console()
        self.current_config = ConfigObj()
        self.client = None
        self.collection = ""
        self.print_greeting()

    def print_missing_config(self) -> None:
        """
        Prints a notice that the configuration is missing and prompts the user
        to attempt to run the 'login' command.
        """
        self.console.print("Try running [bold purple]login[/bold purple]")

    def process_menu_input(self, user_input: str, max_value: int):
        """
        Takes the menu option entered by the user and validates that it can both
        be converted to an integer and is a valid option. All ranges are assumed
        to start at 1.

        Args:
            user_input (str): Menu option entered by the user.
            max_value (int): The maximum value that can be entered.

        Returns:
            int: The integer representation of the user's input, if valid, or 0
            the input was invalid.
        """
        int_value = 0
        try:
            int_value = int(user_input)
            if int_value in range(1, max_value + 1):
                return int_value
        except ValueError:
            # Just pass since the value is initialized to 0.
            pass

        return int_value

    def check_collection(self) -> bool:
        """
        Validates if a collection has been specified or if one is needed. Prints
        a message to the user with what option to select to fix the issue if
        the collection is absent.

        Returns:
            bool: Indicating if there is a collection specified.
        """
        if self.collection == "":
            self.console.print("No [bold purple]collection[/bold purple] has been specified!")
            return False
        else:
            return True

    def get_collection(self) -> None:
        """
        Gets the desired collection from the user.
        """
        # Define the collection.
        self.console.print("Enter the name of the current [bold purple]collection[/bold purple]:")
        self.collection = input("> ")
        self.console.print(f"Saved collection of: [bold purple]{self.collection}[/bold purple]")

    def check_client(self) -> bool:
        """
        Determines if a client has already been instantiated. If not, it creates
        the client, including loading the configuration and the checks which
        go along with that process.

        Returns:
            bool: Indicates if there's currently a client or not.
        """
        if self.client is None:
            # Load the configuration.
            if not self.current_config.load():
                self.print_missing_config()
                return False
            else:
                # Create the client.
                self.client = WriteFreely(
                    self.current_config.instance,
                    self.current_config.access_token,
                    collection=self.collection
                )

                # Ensure the passed collection was valid.
                if not self.client.check_collection():
                    self.console.print("Invalid collection! Specify a new one with option 3.", style="bold red")
                    return False
        return True

    def authenticate(self) -> None:
        """
        Authenticates the user, either creating or overwriting the local
        configuration file.
        """
        auth_obj = Authenticator()
        self.console.print("Enter your instance name.")
        instance = input("> ")
        self.console.print("Enter your username.")
        username = input("> ")
        self.console.print("Enter your password.")
        password = getpass.getpass("> ")
        auth_obj.supply_credentials(
            instance_name=instance,
            user_name=username,
            password=password
        )
        auth_obj.new_login(write_stdout=False)

    def deauthenticate(self) -> None:
        """
        Invalidates any authentication token which may be found and removes the local config file.
        """
        if os.path.isfile(JSON_PATH):
            current_config = dict()
            try:
                with open(JSON_PATH, "r") as config_file:
                    current_config = json.load(config_file)
            except Exception as e:
                self.console.print(f"ERROR: Unable to read {JSON_PATH} with error: {e}", style="bold red")

            if current_config != {} and current_config.get('instance') and current_config.get('access_token'):
                auth_obj = Authenticator()
                try:
                    auth_obj.remove_login(
                        current_config['instance'],
                        current_config['access_token'])
                except KeyError as e:
                    self.console.print("Missing either the instance or access token to log out. Does the config file still exist at: ~/config/writepyly/config.json", style="bold red")
                    sys.exit(1)
                except Exception as e:
                    self.console.print(f"Failed to logout with error: {e}", style="bold red")
                    sys.exit(1)
        else:
            self.console.print(f"No config file found at: {JSON_PATH}")

    def new_post(self, file_name: str) -> None:
        """
        Creates a new post. This method requires the $EDITOR environment
        variable to be set. If it is, then it will automatically open with
        a new temporary file. Once the file is saved, it will be ingested and
        posted. Once the post has been completed, the file is removed.

        Args:
            file_name (str): The name of the temporary file.
        """
        # Launch a sub-process with the user's editor of choice.
        temp_file = f"{TEMP_BASE}/{file_name}"
        # Safe since EDITOR is checked prior to getting here.
        while True:
            editor_result = subprocess.run([os.environ["EDITOR"], temp_file])
            
            # Make sure the editor exited cleanly.
            if editor_result.returncode != 0:
                self.console.print(f"Aborting. Editor exited with code: {editor_result.returncode}", style="bold red")
                return

            # Validate the user still wants to make this post.
            self.console.print("Do you want to publish this post?")
            self.console.print("1. Publish")
            self.console.print("2. Edit")
            self.console.print("3. Discard")
            selection = input("> ")

            if selection == "1" or selection == "3":
                break
            elif selection == "2":
                continue
            else:
                self.console.print("Invalid selection!", style="bold red")


        # Create the post.
        if selection == "1":
            self.console.print("Creating the post...")
            with open(temp_file, "r") as file:
                post_content = file.read()

            # Check if a title was specified.
            post_content_list = post_content.split('\n')
            post_title = None
            if post_content_list[0].startswith('#'):
                post_title = post_content_list[0].replace("#", "").strip()
                post_content_list.remove(post_content_list[0])
                post_content = '\n'.join(post_content_list)

            # Create a post object and validate the collection if one was provided.
            current_post = Post(
                post_content,
                self.current_config.instance,
                self.current_config.access_token,
                collection=self.collection,
                title=post_title)

            # Make the post.
            post_id = current_post.create_post()
            self.console.print(f"Successfully created post with ID: [bold purple]{post_id}[/bold purple]")

        # Delete the file.
        self.console.print(f"Deleting {temp_file}")
        try:
            os.remove(temp_file)
        except Exception as e:
            self.console.print(f"Failed to remove file '{temp_file}' with error: {e}", style="bold red")

    def print_greeting(self):
        """
        Prints a basic greeting to the user.
        """
        self.console.rule("[bold purple]WritePyly :memo:", style="purple")
        self.console.print("[underline]Welcome to the interactive console!")
        self.print_main_menu()

    def print_main_menu(self):
        """
        Prints the main menu to the user and collects input for what the user
        would like to do.
        """
        options = [
            "Login",
            "Logout",
            "Define collection",
            "Create post",
            "Get 10 most recent posts",
            "Delete a post",
            "Quit"]
        while True:
            # Check if there's a collection and get one first if not.
            if self.collection == "":
                self.get_collection()

            counter = 0
            for option in options:
                counter += 1
                self.console.print(f"[bold]{counter}. [/bold]{option}")
            selection = self.console.input("> ")

            # Check if it's valid.
            int_value = self.process_menu_input(selection, len(options))
            if int_value == 0:
                self.console.print(f"[bold red]{selection} is not valid!")
                continue
            else:
                # Call whatever method is required by the user's selection.
                if int_value == 1:
                    # Initiate a new login.
                    self.authenticate()
                elif int_value == 2:
                    # Logout from the current session and remove the configuration.
                    self.deauthenticate()
                elif int_value == 3:
                    # Define the collection.
                    self.get_collection()
                elif int_value == 4:
                    # Ensure we have a collection and client.
                    if self.check_collection() and self.check_client():
                        # Create a new post.
                        if not os.environ.get("EDITOR"):
                            self.console.print("No [bold red]EDITOR[/bold red] found. Be sure this environment variable is set for Unix goodness!")
                        elif not os.path.isdir(TEMP_BASE):
                            self.console.print(f"Temp directory of {TEMP_BASE} doesn't exist!")
                        else:
                            file_name = f"writepyly_{str(uuid.uuid4())}.md"
                            self.console.print(f"Launching your editor with temporary file: [bold purple]{file_name}[/bold purple]")
                            time.sleep(2)
                            self.new_post(file_name)
                elif int_value == 5:
                    # Show the 10 most recent posts.
                    # Check that there's a collection.
                    if self.check_collection() and self.check_client():
                        if self.client is not None:
                            self.client.get_posts()
                        else:
                            self.console.print("We should never get here! Try logging in again...")
                elif int_value == 6:
                    # Delete a post.
                    if self.check_collection() and self.check_client():
                        self.console.print("Enter the post ID to remove.")
                        if self.client is not None:
                            self.client.delete_post(input("> "), exit_on_fail=False)
                        else:
                            # Should never reach but it makes pyright happy.
                            self.console.print("Unable to delete the post as the client still doesn't exist!", style="bold red")
                elif int_value == 7:
                    self.console.print("[bold purple]Goodbye![/bold purple]")
                    sys.exit(0)

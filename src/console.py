import getpass
import sys

from rich.console import Console

from auth import Authenticator
from config import ConfigObj
from client import WriteFreely


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
            self.console.print("No [bold purple]collection[/bold purple] has been specified! Use option 3 first!")
            return False
        else:
            return True

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

    def authenticate(self):
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
                    pass
                elif int_value == 2:
                    # Logout from the current session.
                    pass
                elif int_value == 3:
                    # Define the collection.
                    self.console.print("Enter the name of the current [bold purple]collection[/bold purple]:")
                    self.collection = input("> ")
                    self.console.print(f"Saved collection of: [bold purple]{self.collection}[/bold purple]")
                elif int_value == 4:
                    # Create a new post.
                    pass
                elif int_value == 5:
                    # Show the 10 most recent posts.
                    # Check that there's a collection.
                    if self.check_collection() and self.check_client():
                        if self.client is not None:
                            self.client.get_posts()
                        else:
                            self.console.print("We should never get here! Try logging in again...")
                elif int_value == 6:
                    # Delete a post. Maybe call the 10 most recent automatically?
                    pass
                elif int_value == 7:
                    self.console.print("[bold purple]Goodbye![/bold purple]")
                    sys.exit(0)

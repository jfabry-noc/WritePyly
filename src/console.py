import sys

from rich.console import Console

from auth import Authenticator


class WriteConsole:
    # https://rich.readthedocs.io/en/latest/console.html
    def __init__(self):
        self.console = Console()
        self.print_greeting()

    def process_menu_input(self, user_input: str, max_value: int):
        """
        Takes the menu option entered by the user and validates that it can both
        be converted to an integer and is a valid option. All ranges are assumed
        to start at 1.

        Parameters:
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

    def authenticate(self):
        """
        Authenticates the user, either creating or overwriting the local
        configuration file.
        """

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
            "Create post",
            "Get 10 most recent posts",
            "Delete a post",
            "Quit"]
        counter = 0
        while True:
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
                    pass
                elif int_value == 2:
                    # Logout from the current session.
                    pass
                elif int_value == 3:
                    # Create a new post.
                    pass
                elif int_value == 4:
                    # Show the 10 most recent posts.
                    pass
                elif int_value == 5:
                    # Delete a post. Maybe call the 10 most recent automatically?
                    pass
                elif int_value == 6:
                    self.console.print("[bold purple]Goodbye!")
                    sys.exit(0)


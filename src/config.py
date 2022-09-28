import json
import os

from rich.console import Console

from __init__ import JSON_PATH, WRITEPYLY_PATH


class ConfigObj:
    instance: str
    access_token: str

    def __init__(self):
        self.console = Console()

    def create(self, instance: str, access_token: str) -> None:
        """
        Creates a configuration file with an access token and the desired instance.

        Args:
            instance (str): The instance to use.
            access_token (str): The access token for the Write Freely service.
        """
        config = {"instance": instance, "access_token": access_token}
        json_config = json.dumps(config, indent=4)
        self.create_dir()

        try:
            print(f"Writing JSON configuration to: {JSON_PATH}")
            with open(JSON_PATH, "w") as config_file:
                config_file.write(json_config)
        except Exception as e:
            self.console.print(f"ERROR: Unable to write the config file with error: {e}", style="bold red")

    def delete(self) -> None:
        """
        Deletes the local JSON configuration file if it exists.
        """
        if os.path.isfile(JSON_PATH):
            try:
                os.remove(JSON_PATH)
            except Exception as e:
                self.console.print(f"Unable to remove the config file with error: {e}", style="bold red")

    def create_dir(self) -> None:
        """
        Creates the directory used to store the configuration file if it doesn't
        already exist.
        """
        if not os.path.isdir(WRITEPYLY_PATH):
            try:
                self.console.print(f"Creating config directory at: [bold purple]{WRITEPYLY_PATH}[/bold purple]")
                os.makedirs(WRITEPYLY_PATH)
            except Exception as e:
                self.console.print("ERROR: Unable to create the config directory at:", style="bold red")
                self.console.print(f"\t{WRITEPYLY_PATH}", style="bold red")
                self.console.print(f"\nWith error: {e}", style="bold red")

    def load(self) -> bool:
        """
        Loads the JSON configuration, storing the instance and access token to the
        `instance` and `access_token` properties of the current object.

        Returns:
            bool: Indicates whether or not the operation was successful.
        """
        if os.path.isfile(JSON_PATH):
            with open(JSON_PATH, "r") as file:
                configuration = json.load(file)
                self.instance = configuration.get("instance")
                self.access_token = configuration.get("access_token")

            if self.instance is None:
                self.console.print(f"ERROR loading configuration file at: {JSON_PATH}", style="bold red")
                self.console.print("File was found, but 'instance' is missing.", style="bold red")
                return False
            elif self.access_token is None:
                self.console.print(f"ERROR loading configuration file at: {JSON_PATH}", style="bold red")
                self.console.print("File was found, but 'access_token' is missing.", style="bold red")
                return False
            else:
                return True
        else:
            self.console.print(f"No configuration file to load at: {JSON_PATH}", style="bold red")
            self.console.print("Do you need to run 'writepyly login' or use the 'login' command from interactive mode?", style="red")
            return False

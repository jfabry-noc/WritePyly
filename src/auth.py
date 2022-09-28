import json
import sys

import requests

from config import ConfigObj
from rich.console import Console


class Authenticator():
    def __init__(self):
        self.console = Console()

    def supply_credentials(self, instance_name: str, user_name: str, password: str) -> None:
        self.instance_name = instance_name
        self.user_name = user_name
        self.password = password

    def remove_login(self, instance_name: str, access_token: str) -> None:
        """
        Invalidates an existing access token and removes the JSON file storing it.

        Args:
            instance_name (str): Name of the instance associated with the token.
            access_token (str): Value of the access token to invalidate.
        """
        # Invalidate the existing token.
        logout_url = f"https://{instance_name}/api/auth/me"
        print(f"Using logout URL: {logout_url}")
        try:
            logout_response = requests.delete(
                url=logout_url,
                headers={"Authorization": f"Token {access_token}"}
                )

            if logout_response.status_code == 204:
                print("Successfully logged out. Removing local files...")
            else:
                print(f"Logout attempt unsuccessful with response: {logout_response.status_code}")
                print("Proceeding with local file removal...")
        except Exception as e:
            print(f"Unable to log out with access token \"{access_token}\".")
            print(f"Error was: {e}")
            print("Proceeding with removal of local files...")

        # Delete the local configuration.
        current_config = ConfigObj()
        current_config.delete()

    def new_login(self, write_stdout: bool = True):
        """
        Makes the authentication request.
        """
        if write_stdout:
            print(f"Attempting login with username {self.user_name}, password {self.password}, and instance {self.instance_name}")
        try:
            login_url = f"https://{self.instance_name}/api/auth/login"
            login_dto = json.dumps({"alias": self.user_name, "pass": self.password})
            if write_stdout:
                print(f"Login DTO is: {login_dto}")
            auth_response = requests.post(
                url=login_url,
                data=login_dto,
                headers={"Content-Type": "application/json"}
                )

            if write_stdout:
                print(f"JSON response is: {auth_response.json()}")
            if auth_response.status_code == 200:
                access_token = auth_response.json().get('data').get('access_token')

                # Save the access token and instance.
                if access_token:
                    current_config = ConfigObj()
                    current_config.create(self.instance_name, access_token)
                else:
                    if write_stdout:
                        self.console.print(f"[bold red]ERROR:[/bold red] Server response was 200 but no access token was provided.")
                        print(f"Full body was:\nf{auth_response.json()}")
            else:
                self.console.print(f"[bold red]Unsuccessful authentication with response code: {auth_response.status_code}[/bold red]")
                if write_stdout:
                    sys.exit(1)
        except Exception as e:
            self.console.print(f"[bold red]ERROR:[/bold red] Unable to authenticate with error: {e}")


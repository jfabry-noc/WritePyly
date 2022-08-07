import json
import os
import sys

from __init__ import CONFIG_PATH, JSON_PATH, WRITEPYLY_PATH


class ConfigObj:
	instance: str
	access_token: str

	def create(self, instance: str, access_token: str):
		config = {"instance": instance, "access_token": access_token}
		json_config = json.dumps(config, indent=4)
		self.create_dir()

		try:
			print(f"Writing JSON configuration to: {JSON_PATH}")
			with open(JSON_PATH, "w") as config_file:
				config_file.write(json_config)
		except Exception as e:
			print(f"ERROR: Unable to write the config file with error: {e}")

	def delete(self):
		if os.path.isfile(JSON_PATH):
			try:
				os.remove(JSON_PATH)
			except Exception as e:
				print(f"Unable to remove the config file with error: {e}")

	def create_dir(self):
		if not os.path.isdir(WRITEPYLY_PATH):
			try:
				print(f"Creating config directory at: {WRITEPYLY_PATH}")
				os.makedirs(WRITEPYLY_PATH)
			except Exception as e:
				print("ERROR: Unable to create the config directory at:")
				print(f"\t{WRITEPYLY_PATH}")
				print(f"\nWith error: {e}")

	def load(self):
		if os.path.isfile(JSON_PATH):
			instance = ""
			access_token = ""
			with open(JSON_PATH, "r") as file:
				configuration = json.load(file)
				print(f"Adding instance to the config: {configuration.get('instance')}")
				self.instance = configuration.get("instance")
				print(f"Adding access token to the config: {configuration.get('access_token')}")
				self.access_token = configuration.get("access_token")

			if self.instance is None:
				print(f"ERROR loading configuration file at: {JSON_PATH}")
				print("File was found, but 'instance' is missing. Please re-run 'writepyly login'.")
				sys.exit(1)
			elif self.access_token is None:
				print(f"ERROR loading configuration file at: {JSON_PATH}")
				print("File was found, but 'access_token' is missing. Please re-run 'writepyly login'.")
				sys.exit(1)
		else:
			print(f"No configuration file to load at: {JSON_PATH}")
			print("Do you need to run 'writepyly login'?")

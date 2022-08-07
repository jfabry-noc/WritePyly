import json
import os

from __init__ import JSON_PATH, WRITEPYLY_PATH

class ConfigObj:
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

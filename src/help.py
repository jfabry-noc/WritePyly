class Helper:
	"""
	Container for the various help methods displayed in conjunction with different
	CLI options, e.g.

	writepyly help
	writepyly help login
	writepyly help post
	"""
	def help_empty(self):
		print("writepyly - CLI tool for posting to a Write Freely instance.")
		print("\n\twritepyly help | login | logout | post")
		print("\nHelp can be combined with other commands for additional detail:")
		print("\n\twritepyly help login\n")

	def help_login(self):
		print("The login command requires credentials in the form of a username,")
		print("password, and instance. These credentials are NOT stored locally,")
		print("though the resulting API key will be stored in:")
		print("\n\t~/.config/writepyly/config.json")
		print("\nYou can delete this file to clear the config, though it's")
		print("recommended to run \"writepyly logout\" instead as this will")
		print("invalidate the key against the server first!")
		print("\nThe username should be passed first, followed by the password")
		print("and then the instance:")
		print("\n\twritepyly login username password instance")
		print("\nAny existing authentication configuration will be overwritten,")
		print("and an attempt will be made to invalidate any old keys first.")
		print("\nThe instance should be entered without any protocol information")
		print("as just the DNS value, e.g.: write.as")
		print("\n\twritepyly login myusername password123 write.as")
		print("\nBe aware that if you have a strong password with special characters")
		print("you may need to wrap it in single quotes so that it is treated")
		print("literally by your shell.")

	def help_logout(self):
		print("The logout command requires no additional parameters. It will")
		print("attempt to invalidate any existing keys, though if that isn't")
		print("possible, e.g. if the command is run while offline, it will move")
		print("forward with deleting the configuration file:")
		print("\n\twritepyly logout")
		print("\nThe configuration file is located at:")
		print("\n\t~/.config/writepyly/config.json\n")

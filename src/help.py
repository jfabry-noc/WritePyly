class Helper:
    """
    Container for the various help methods displayed in conjunction with different
    CLI options, e.g.

    writepyly help
    writepyly help login
    writepyly help post
    """
    def help_empty(self) -> None:
        """
        Help message when nothing is passed as an additional parameter:

        `writepyly help`
        """
        print("writepyly - CLI tool for posting to a Write Freely instance.")
        print("\n\twritepyly help | login | logout | post | get | delete")
        print("\nHelp can be combined with other commands for additional detail:")
        print("\n\twritepyly help login\n")

    def help_login(self) -> None:
        """
        Help message when `login` is passed as an additional parameter:

        `writepyly help login`
        """
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

    def help_logout(self) -> None:
        """
        Help message when `logout` is passed as an additional parammeter.

        `writepyly help logout`
        """
        print("The logout command requires no additional parameters. It will")
        print("attempt to invalidate any existing keys, though if that isn't")
        print("possible, e.g. if the command is run while offline, it will move")
        print("forward with deleting the configuration file:")
        print("\n\twritepyly logout")
        print("\nThe configuration file is located at:")
        print("\n\t~/.config/writepyly/config.json\n")

    def help_post(self) -> None:
        """
        Help message when `post` is passed as an additional parameter:

        `writepyly help post`
        """
        print("Posting requires the content to post. Content may be specified")
        print("either via a path to the Markdown file or pipe through STDIN.")
        print("File paths can either be full or relative.")
        print("\nOptionally, you may also include the collection (or blog) you")
        print("wish to post the content to.")
        print("\nThis example shows posting via a Markdown file path to the")
        print("blog named 'api-tester':")
        print("\n\twritepyly post ../sample_data/test_post.md api-tester")
        print("\nThis example shows the same as above, but the post content")
        print("is submitted via STDIN:")
        print("\n\tcat ../sample_data/test_post.md | writepyly post -- api-tester\n")

    def help_get(self) -> None:
        """
        Help message when `get` is passed as an additional parameter.

        `writepyly help get`
        """
        print("Returns the title, post date, and ID of your posts at the specified")
        print("collection. ONLY collections can be queried for posts, so the")
        print("collection name must be included. As the API will return only")
        print("the last 10 posts, that's how many will be displayed here.")
        print("\n\twritepyly get {collection}\n")

    def help_delete(self) -> None:
        """
        Help message when `delete` is passed as an additional parameter.

        `writepyly help delete`
        """
        print("Requires a post ID to be given as a parameter after the delete")
        print("command:")
        print("\n\twritepyly delete {post_id}\n")
        print("Post IDs can be obtained from:")
        print("\n\twritepyly get\n")
        print("For additional information see:")
        print("\n\twritepyly help get")

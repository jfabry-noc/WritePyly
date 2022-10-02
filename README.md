# WritePyly

Project to create a Python CLI and TUI client for Write.as/WriteFreely instances.

## Description

The goal of the project is to provide a simple CLI client for pushing content to a WriteFreely instance, deleting posts from that instance, etc. In the future, I'd like to add functionality to create a TUI when no arguments are passed. It will also (hopefully) be distributed via [PyPI](https://pypi.org/) once it gets to a point where I feel like that's warranted.

## Installation

Since this is still an early work in progress, all of this is subject to change as it matures. Currently you'll need to clone the repo directly:

```shell
git clone https://gitlab.com/loopednetwork/writepyly.git
````

Once in the project directory from the CLI, just run the setup script:

```shell
./setup.sh
```

This only works with POSIX systems. If you happen to be running this on Windows, there are assumptions made in the code which mean it probably won't work even if you get the setup deployed. I don't have a Windows system to test with.

## Usage

If you've run `setup.sh`, you should have a `writepyly` executable available on your `PATH`. This can be validated by running:

```shell
which writepyly
```

If you get output (which should be `/usr/local/bin/writepyly`), then everything is set. If there's no output, then something has gone wrong.

The main options offered currently are:

- `help`
- `get`
- `login`
- `logout`
- `post`
- `get`
- `delete`

### `help`

This displays the help information running it by itself...

```shell
writepyly help
```

... will show the generic help message. It can be combined with any of the commands above to display additional, more specific information. For example, to show more details on the `post` command, run:

```shell
writepyly help post
```

### `get`

This retrieves the 10 most recent posts from a collection and displays:

- title
- creation date
- ID

If the post has an actual title, that will be displayed. Otherwise, the first 50 character of the post will be shown instead. The main use case is to get an ID for post management. Assuming the collection is [api-tester](https://apitester.looped.network/), the command would be:

```shell
writepyly get api-tester
```

As the API will only give back the most recent 10, there are no other options for the number of posts, paging, etc.

### `login`

This is used to either log in for the first time or to overwrite the current login information. Logging in reqires providing:

- username
- password
- instance

__Note__: The main goal currently isn't anonymous posting, so you may see weird, untested behavior if you try doing anything without authentication.

The "username" and "password" are what you would normally use to log in to your WriteFreely instance. The instance itself is the domain name (sans any protocol, like `https`) you use. If you're a [Write.as](https://write.as/) user, for example, then the instance is just `write.as`. It's important to note that the instance is the domain where you _actually_ authenticate. For example, if you're a Write.as user with a custom domain configured, you would still use `write.as` as the instance since that's where authentication happens.

Authentication commands should look like:

```shell
writepyly {username} {password} {instance}
```

For example, to log in to `write.as` as the user `looped`, run:

```shell
writepyly looped Abc123 write.as
```

The credentials are **not** stored locally, though the access token received in response is. It will be placed into the following file:

`~/.config/writepyly/config.json`

If you want to remove authorization, you should **not** delete the above file. Instead, run the `logout` command.

### `logout`

This command will first attempt to invalidate its locally cached access token against the instance in use. Regardless of the success or failure, the locally cached token and instance are then removed, as the following file is deleted:

`~/.config/writepyly/config.json`

It's highly recommended to use this command rather than deleting the file manually, as then the access token is still valid on the server side.

### `post`

This command allows for new posts to be submitted. There are two primary options:

- Provide the path to a Markdown file with the content to post.
- Read content from STDIN through the pipeline.

Paths to Markdown files can be either fully qualified or relative. For example, to use a Markdown file located in a directory up in a folder called `sample_data` which is named `test_post.md`, enter:

```shell
writepyly post ../sample_data/test_post.md
```

This will publish anonymously and is currently untested functionality. To publish to a collection you own, simply append the collection name as an additional parameter, such as this example where we're posting to the collection called `api-tester`:

```shell
writepyly post ../sample_data/test_post.md api-tester
```

If reading from STDIN, just replace the file path with `--`. The following command would achieve the same as the command above:

```shell
cat ../sample_data/test_post.md | writepyly post -- api-tester
```

### `delete`

This command will delete a given post. It requires a post ID as a parameter:

```shell
writepyly delete {post_id}
```

To easily retrieve a post ID, use the `get` command.

## TUI

In addition to the CLI client described above, there is also a TUI client available by simply running `writepyly` with no arguments. This will drop you into an interactive mode. The first thing you'll be prompted for is the collection to use, though this can be changed later.

The options for the TUI client are clearly laid out in the menu which is displayed. They mirror the functionality of the CLI version. The only thing worth mentioning is that creating a new post will require the `$EDITOR` environment variable to be set so that `writepyly` knows what to use for creating the content. If that isn't set, you'll be notified about it. It can easily be set by adding something like the following to your `~/.profile`, `~/.zshrc`, etc. file, depending on what your `$SHELL` is:

```shell
export EDITOR="/usr/bin/vim"
```

## Project status

This project is more or less wrapped up since it currently meets my needs. If I think of other features or if someone requests something additional, though, I'll certainly be willing to look at adding it. 💜

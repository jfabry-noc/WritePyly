import requests
import sys

from rich.console import Console


class WriteFreely:
    def __init__(self, instance: str, access_token: str, **kwargs):
        self.instance = instance
        self.access_token = access_token
        if kwargs.get("collection"):
            self.collection = kwargs.get("collection")
        self.console = Console()

    def check_collection(self) -> bool:
        """
        Checks for the presence of a collection to assert that a specified
        collection is valid.

        Returns:
            bool: Indicates if the client exists (`True`) or not (`False`)
        """
        if self.collection:
            try:
                collection_url = f"https://{self.instance}/api/collections/{self.collection}"
                # Get the user's collections and validate that this is one of them.
                collection_response = requests.get(
                    url=collection_url,
                    headers={"Content-Type": "application/json",
                        "Authorization": f"Token {self.access_token}"})

                if collection_response.status_code != 200:
                    self.console.print(f"Error: Specified collection of {self.collection} is not valid!", style="bold red")
                    self.console.print(f"Are you sure you have the correct name for your collection?")
                    return False
            except Exception as e:
                self.console.print(f"Error attempting to check validity of collection: {self.collection}", style="bold red")
                self.console.print(f"Error was: {e}", style="bold red")
                return False

            return True
        else:
            return False

    def get_posts(self):
        """
        Gets the posts from a collection, printing their titles, IDs, and
        publication dates. Content will be sorted with the newest posts appearing
        first. The first 10 posts are returned, matching what the API responds with.
        """
        post_url = f"https://{self.instance}/api/collections/{self.collection}/posts"

        # Retrieving content from public collections doesn't require authentication
        # but do it anyway in case future limits impede the number of calls since
        # we can't make it to this point without valid authentication anyway.
        try:
            collection_results = requests.get(
                post_url,
                headers={
                "Content-Type": "application/json",
                "Authorization": f"Token: {self.access_token}"
                })
        except Exception as e:
            self.console.print(f"Failed to retrieve posts with error: {e}", style="bold red")
            sys.exit(1)

        # Process the results.
        post_list = list()
        for single_post in collection_results.json().get('data').get('posts'):
            current_title = ""
            if single_post.get('title'):
                current_title = single_post.get('title')
            elif len(single_post.get('body')) <= 50:
                current_title = single_post.get('body').strip().replace("\n", " ")
            else:
                current_title = single_post.get('body')[0:47].strip().replace("\n", " ") + "..."
            post_list.append({
                "title": current_title,
                "created": single_post.get('created'),
                "id": single_post.get('id')})

        sorted_posts = sorted(post_list, key = lambda p: p['created'], reverse=True)

        # Process how to render them.
        for single_post in sorted_posts:
            # Print the current post to STDOUT.
            self.console.print(f"[bold purple]Title:[/bold purple]   [white]{single_post.get('title')}[/white]")
            self.console.print(f"[bold purple]Created:[/bold purple] [white]{single_post.get('created')}[/white]")
            self.console.print(f"[bold purple]ID:[/bold purple]      [white]{single_post.get('id')}[/white]\n")

    def delete_post(self, post_id: str, exit_on_fail=True):
        """
        Deletes a post via the post ID. Most commonly retrieved from running the
        'get' command.

        Args:
            post_id (str): ID of the post to remove.
        """
        delete_url = f"https://{self.instance}/api/posts/{post_id}"
        try:
            deletion_response = requests.delete(
                delete_url,
                headers={
                "Content-Type": "application/json",
                "Authorization": f"Token {self.access_token}"
                })

            # Validate the deletion was successful.
            if deletion_response.status_code == 204:
                self.console.print(f"Successfully deleted post: [bold purple]{post_id}[/bold purple]")
            else:
                self.console.print(f"Failed to delete post {post_id} with status code: {deletion_response.status_code}", style="bold red")
        except Exception as e:
            self.console.print(f"Failed to delete post with ID: {post_id}", style="bold red")
            self.console.print(f"Error was: {e}", style="bold red")
            if exit_on_fail:
                sys.exit(1)

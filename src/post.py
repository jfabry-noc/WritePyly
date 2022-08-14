import json
import requests
import sys

from client import WriteFreely


class Post(WriteFreely):
	def __init__(self, post_content: str, instance: str, access_token: str, **kwargs):
		self.post_content = post_content
		self.instance = instance
		self.access_token = access_token
		if kwargs.get('collection'):
			self.collection = kwargs.get('collection')
		if kwargs.get('title'):
			self.title = kwargs.get('title')
		else:
			self.title = None

	def create_post(self) -> str:
		"""
		Submits the post to the Write Freely instance.

		Returns:
			str: The ID of the post.
		"""
		# Determine the URL.
		post_url = ""
		if self.collection != "":
			post_url = f"https://{self.instance}/api/collections/{self.collection}/posts"
		else:
			post_url = f"https://{self.instance}/api/posts"

		# Put together the post DTO. This will need to change a LOT.
		post_dict = {"body": self.post_content}
		if self.title is not None and self.title != "":
			post_dict['title'] = self.title
		post_dto = json.dumps(post_dict)
		print(f"Posting: {post_dto}")

		# Submit the post.
		try:
			post_response = requests.post(
				url=post_url,
				headers={"Content-Type": "application/json",
					"Authorization": f"Token {self.access_token}"},
					data=post_dto
					)

			if post_response.status_code == 201:
				post_id = post_response.json().get('data').get('id')
				if post_id:
					return post_id
				else:
					print(f"No post ID found. Full response was: {post_response.json()}")
					sys.exit(1)
			else:
				print(f"Post unsuccessful with status code: {post_response.status_code}")
				sys.exit(1)
		except Exception as e:
			print(f"ERROR: Post attempt failed with error: {e}")
			sys.exit(1)

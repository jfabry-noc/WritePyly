import requests

class WriteClient:
    def __init__(self, instance_name: str, access_token: str = "", user_name: str = "", password: str = ""):
        self.instance_name = instance_name
        self.user_name = user_name
        self.password = password
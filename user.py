from flask_login import UserMixin

users = {"demo": {"password": "demo_project"},
         "pmr": {"password": "pmrresearch"}}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

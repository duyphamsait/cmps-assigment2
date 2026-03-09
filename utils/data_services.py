import os
import json
from typing import List, Optional
from models.user import User

MAX_ATTEMPT = 3


class DataServices:
    def __init__(self, json_path: str = None):
        if json_path is None:
            base_dir = os.path.dirname(__file__)
            json_path = os.path.join(base_dir, "mock_data.json")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.users: List[User] = [User(**u) for u in data.get("users", [])]

    def find_user_by_username(self, username: str) -> Optional[User]:
        usr = username.strip()
        return next((u for u in self.users if u.username == usr), None)

    def login(self, username: str, password: str):
        username = (username or "").strip()
        password = (password or "").strip()

        user = next((u for u in self.users if u.username == username), None)

        if user is None:
            return False, "User does not exist.", None

        if not user.active:
            return False, "Account is inactive.", None

        if user.password != password:
            user.login_attempts += 1
            user.logged_in = False

            if user.login_attempts >= MAX_ATTEMPT:
                user.active = False
                return False, "Too many failed login attempts. Account locked.", None

            return False, "Wrong username or password.", None

        user.login_attempts = 0
        user.logged_in = True

        return True, "Login successful.", user

    def logout(self, user: User):
        if user:
            user.logged_in = False
            return True, "Logout successful."
        return False, "Logout failed."
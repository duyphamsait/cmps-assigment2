from dataclasses import dataclass
from typing import List
from models.role import Role

@dataclass
class User:
    uid: int
    username: str
    password: str
    role: Role
    subscription: str
    logged_in: bool
    login_attempts: int
    active: bool

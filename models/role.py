from enum import Enum


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class Feature(str, Enum):
    MANAGE_USERS = "Manage Users"
    EDIT_POSTS = "Edit Posts"
    VIEW_POSTS = "View Posts"


role_features = {
    Role.ADMIN: [
        Feature.MANAGE_USERS
    ],
    Role.EDITOR: [
        Feature.EDIT_POSTS,
        Feature.VIEW_POSTS
    ],
    Role.VIEWER: [
        Feature.VIEW_POSTS
    ]
}
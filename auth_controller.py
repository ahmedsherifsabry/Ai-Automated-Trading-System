# controllers/auth_controller.py

from services.user_service import UserService


def login_user(username: str, password: str):
    return UserService.login(username, password)


def register_user(username: str, password: str):
    return UserService.register(username, password)

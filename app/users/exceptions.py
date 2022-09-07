from fastapi import HTTPException


class LoginRequiredException(HTTPException):
    # status_code = 401
    # detail = "Login required"
    pass

# class LoginRequiredException(Exception):
#     pass


class UserHasAccountException(Exception):
    """User already has account."""


class InvalidEmailException(Exception):
    """Invalid email"""


class InvalidUserIDException(Exception):
    """Invalid user id"""

import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from app.users import validators
from app.users.exceptions import (
    InvalidEmailException,
    UserHasAccountException,
    # InvalidUserIDException
)


class User(Model):
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"

    @staticmethod
    def create_user(email, password=None):
        q = User.objects.filter(email=email)
        if q.count() != 0:
            raise UserHasAccountException("User with this email already exists.")
        valid, msg, email = validators.validate_email_(email)
        if not valid:
            raise InvalidEmailException(f"Invalid Email: {msg}")
        obj = User(email=email)
        obj.password = password
        obj.save()
        return obj

import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app.core.config import get_settings
from app.users import validators, security
from app.users.exceptions import (
    InvalidEmailException,
    UserHasAccountException,
    # InvalidUserIDException
)

settings = get_settings()


class User(Model):
    __keyspace__ = settings.keyspace
    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    password = columns.Text()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"User(email={self.email}, user_id={self.user_id})"

    def set_password(self, password, commit=False):
        self.password = security.generate_hash(password)
        if commit:
            self.save()
        return True

    def verify_password(self, password_raw):
        password_hash = self.password
        verified, _ = security.verify_hash(password_hash, password_raw)
        return verified

    @staticmethod
    def create_user(email, password=None):
        q = User.objects.filter(email=email)
        if q.count() != 0:
            raise UserHasAccountException("User with this email already exists.")
        valid, msg, email = validators.validate_the_email(email)
        if not valid:
            raise InvalidEmailException(f"Invalid Email: {msg}")
        obj = User(email=email)
        obj.set_password(password)
        obj.save()
        return obj

    @staticmethod
    def check_exists(user_id):
        q = User.objects.filter(user_id=user_id).allow_filtering()
        return q.count() != 0

    @staticmethod
    def get_by_user_id(user_id=None):
        if user_id is None:
            return None
        q = User.objects.filter(user_id=user_id).allow_filtering()
        if q.count() != 1:
            return None
        return q.first()

import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app.core.config import get_settings
from app.users.models import User
from app.videos.extractors import extract_video_id

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.keyspace
    host_id = columns.Text(primary_key=True)
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    host_service = columns.Text(default='youtube')
    title = columns.Text()
    url = columns.Text()
    user_id = columns.UUID()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Video(title={self.title}, host_id={self.host_id}, host_service={self.host_service})"

    @staticmethod
    def add_video(url, user_id=None):
        host_id = extract_video_id(url)
        if host_id is None:
            raise Exception("Invalid Youtube Video URL")
        user_id_exists = User.check_exists(user_id)
        if user_id_exists is None:
            raise Exception("Invalid User ID")
        q = Video.objects.allow_filtering().filter(
            host_id=host_id,
            # Add below line if you want to restrict videos to a specific user, that is not the case now.
            user_id=user_id
        )
        if q.count() != 0:
            raise Exception("Video already exists.")
        return Video.create(host_id=host_id, user_id=user_id, url=url)

# class PrivateVideo(Video):
#     pass

import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from app.core.shortcuts import templates
from app.core.config import get_settings
from app.users.exceptions import InvalidUserIDException
from app.users.models import User
from app.videos.exceptions import VideoAlreadyAddedException, InvalidYouTubeVideoURLException
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

    def render(self):
        basename = self.host_service
        template_name = f"/videos/renderers/{basename}.html"
        context = {"host_id": self.host_id}
        t = templates.get_template(template_name)
        return t.render(context)

    def as_data(self):
        return {
            f"{self.host_service}_id": self.host_id,
            "path": self.path,
            "title": self.title
        }

    @property
    def path(self):
        return f"/videos/{self.host_id}"

    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        host_id = extract_video_id(url)
        if host_id is None:
            raise InvalidYouTubeVideoURLException("Invalid Youtube Video URL")
        user_id_exists = User.check_exists(user_id)
        if user_id_exists is None:
            raise InvalidUserIDException("Invalid User ID")
        q = Video.objects.allow_filtering().filter(
            host_id=host_id,
            # MultipleObjectsReturned Exception - no duplicate video
            # user_id=user_id
        )
        if q.count() != 0:
            raise VideoAlreadyAddedException("Video already exists.")
        return Video.create(host_id=host_id, user_id=user_id, url=url, **kwargs)

# class PrivateVideo(Video):
#     pass

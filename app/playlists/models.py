import uuid
from datetime import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app.core import config
from app.videos.models import Video

settings = config.get_settings()


class Playlist(Model):
    __keyspace__ = settings.keyspace
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    user_id = columns.UUID()
    updated = columns.DateTime(default=datetime.utcnow())
    host_ids = columns.List(value_type=columns.Text)
    title = columns.Text()

    def add_host_ids(self, host_ids=None, replace_all=False):
        if host_ids is None:
            host_ids = []
        if not isinstance(host_ids, list):
            return False
        if replace_all:
            self.host_ids = host_ids
        else:
            self.host_ids += host_ids
        self.updated = datetime.utcnow()
        self.save()
        return True

    def get_videos(self):
        videos = []
        for host_id in self.host_ids:
            try:
                video_obj = Video.objects.get(host_id=host_id)
            except:
                video_obj = None
            if video_obj is not None:
                videos.append(video_obj)
        return videos

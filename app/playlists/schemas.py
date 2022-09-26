import uuid
from app.videos.extractors import extract_video_id
from pydantic import BaseModel, validator, root_validator
from app.videos.models import Video
from app.playlists.models import Playlist


class PlaylistCreateSchema(BaseModel):
    title: str
    user_id: uuid.UUID

class PlaylistVideoAddSchema(BaseModel):
    url: str
    title: str
    user_id: uuid.UUID
    playlist_id: uuid.UUID

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        url = v
        video_id = extract_video_id(url)
        if video_id is None:
            raise ValueError(f"{url} is not a valid Youtube URL.")
        return url

    @validator("playlist_id")
    def validate_playlist_id(cls, v, values, **kwargs):
        q = Playlist.objects.filter(db_id=v)
        if q.count() == 0:
            raise ValueError(f"{v} is not a valid Playlist.")
        return v

    @root_validator
    def validate_data(cls, values):

        url = values.get("url")
        if url is None:
            raise ValueError("A valid URL is required.")

        title = values.get("title")
        playlist_id = values.get("playlist_id")
        user_id = values.get("user_id")

        video_obj = None

        extra_data = {}
        if title is not None:
            extra_data['title'] = title

        try:
            video_obj, created = Video.get_or_create(url, user_id=user_id, **extra_data)
        except Exception:
            raise ValueError("There's a problem with your account, please try again.")
        if not isinstance(video_obj, Video):
            raise ValueError("There's a problem with your account, please try again.")
        else:
            playlist_obj = Playlist.objects.get(db_id=playlist_id)
            playlist_obj.add_host_ids(host_ids=[video_obj.host_id])
            playlist_obj.save()
        return video_obj.as_data()

import uuid

from pydantic import BaseModel

# from app.playlists.models import Playlist


class PlaylistCreateSchema(BaseModel):
    title: str
    user_id: uuid.UUID


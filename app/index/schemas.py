import uuid
from typing import Union

from pydantic import BaseModel, Field, root_validator, validator


class VideoIndexSchema(BaseModel):
    objectID: str = Field(alias='host_id')
    objectType: str = 'Video'
    title: Union[str, None]
    path: str = Field(alias='host_id')

    # TODO related -> playlist names

    @validator("path")
    def set_path(cls, v, values, **kwargs):
        host_id = v
        return f"/videos/{host_id}"


class PlaylistIndexSchema(BaseModel):
    objectID: uuid.UUID = Field(alias='db_id')
    objectType: str = 'Playlist'
    title: Union[str, None]
    path: str = Field(default='/')

    # TODO - related -> host_ids -> Video Title

    @root_validator
    def set_defaults(cls, values):
        object_id = values.get('objectID')
        values["objectID"] = str(object_id)
        values['path'] = f"/playlists/{object_id}"
        return values

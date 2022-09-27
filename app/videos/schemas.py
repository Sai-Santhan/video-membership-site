import uuid

from pydantic import BaseModel, validator, root_validator

from app.users.exceptions import InvalidUserIDException
from app.videos.exceptions import InvalidYouTubeVideoURLException, VideoAlreadyAddedException
from app.videos.extractors import extract_video_id
from app.videos.models import Video


class VideoCreateSchema(BaseModel):
    url: str
    title: str
    user_id: uuid.UUID

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        video_id = extract_video_id(v)
        if video_id is None:
            raise ValueError(f"{v} is not a valid YouTube URL")
        return v

    @root_validator()
    def validate_data(cls, values):
        url = values.get("url")
        if url is None:
            raise ValueError("A valid URL is required.")
        title = values.get("title")
        user_id = values.get("user_id")
        video_obj = None
        extra_data = {}
        if title is not None:
            extra_data['title'] = title
        try:
            video_obj = Video.add_video(url, user_id=user_id, **extra_data)
        except InvalidYouTubeVideoURLException:
            raise ValueError(f"{url} is not a valid YouTube URL")
        except VideoAlreadyAddedException:
            raise ValueError(f"{url} has already been added to your account.")
        except InvalidUserIDException:
            raise ValueError("There's a problem with your account, please try again.")
        except Exception:
            raise ValueError("There's a problem with your account, please try again.")
        if video_obj is None:
            raise ValueError("There's a problem with your account, please try again.")
        if not isinstance(video_obj, Video):
            raise ValueError("There's a problem with your account, please try again.")
        # if title is not None:
        #     video_obj.title = title
        #     video_obj.save()
        return video_obj.as_data()


class VideoEditSchema(BaseModel):
    url: str
    title: str

    @validator("url")
    def validate_youtube_url(cls, v, values, **kwargs):
        video_id = extract_video_id(v)
        if video_id is None:
            raise ValueError(f"{v} is not a valid YouTube URL")
        return v
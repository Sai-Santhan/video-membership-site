from typing import Union

from pydantic import BaseModel


class WatchEventSchema(BaseModel):
    host_id: str
    path: Union[str, None]
    start_time: float
    end_time: float
    duration: float
    complete: bool

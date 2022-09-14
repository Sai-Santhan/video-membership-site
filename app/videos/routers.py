from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.shortcuts import render
from app.videos.models import Video

router = APIRouter(
    prefix="/videos"
)


@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    q = Video.objects.all().limit(100)
    context = {
        "object_list": q,
    }
    return render(request, "videos/list.html", context)

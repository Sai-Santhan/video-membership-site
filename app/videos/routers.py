from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core.shortcuts import render
from app.users.decorators import login_required
from app.videos.models import Video

router = APIRouter(
    prefix="/videos"
)


@router.get("/create", response_class=HTMLResponse)
@login_required
def video_create_view(request: Request):
    return render(request, "videos/create.html")


@router.get("/", response_class=HTMLResponse)
def video_list_view(request: Request):
    q = Video.objects.all().limit(100)
    context = {
        "object_list": q,
    }
    return render(request, "videos/list.html", context)


@router.get("/detail", response_class=HTMLResponse)
def video_detail_view(request: Request):
    return render(request, "video/detail.html")

import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import EmailStr, SecretStr
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.authentication import AuthenticationMiddleware

from app.core import db, utils
from app.core.shortcuts import render, redirect
from app.users.backends import JWTCookieBackend
from app.users.decorators import login_required
from app.users.exceptions import LoginRequiredException
from app.users.models import User
from app.users.schemas import UserSignupSchema, UserLoginSchema
from app.videos.models import Video
from app.videos.routers import router as video_router
from app.watch_events.models import WatchEvent

DB_SESSION = None

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    status_code = exc.status_code
    template_name = 'errors/main.html'
    if status_code == 404:
        template_name = 'errors/404.html'
    context = {"status_code": status_code}
    return render(request, template_name, context, status_code=status_code)


@app.exception_handler(LoginRequiredException)
async def login_required_exception_handler(request, exc):
    return redirect(f"/login?next={request.url}", remove_session=True)


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)
    sync_table(WatchEvent)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", status_code=200)
    return render(request, "home.html")


@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    return render(request, "account.html")


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    return render(request, "auth/login.html")


@app.post("/login", response_class=HTMLResponse)
def login_post_view(request: Request,
                    email: EmailStr = Form(...),
                    password: SecretStr = Form(...)):
    raw_data = {
        "email": email,
        "password": password,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "auth/login.html", context)
    return redirect("/", cookies=data)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/signup.html")


@app.post("/signup", response_class=HTMLResponse)
def signup_post_view(request: Request,
                     email: EmailStr = Form(...),
                     password: SecretStr = Form(...),
                     password_confirm: SecretStr = Form(...)):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "auth/signup.html", context)
    return redirect("/login")


@app.get("/users/")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)


@app.post("/watch-event")
def watch_event_view(request: Request, data: dict):
    if request.user.is_authenticated:
        WatchEvent.objects.create(
            host_id=data.get("videoId"),
            user_id=request.user.username,
            start_time=0,
            end_time=data.get('currentTime'),
            duration=500,
            complete=False
        )
    return {"working": True}


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

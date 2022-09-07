import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.core import db
from app.core.shortcuts import render
from app.users.models import User

DB_SESSION = None

app = FastAPI()


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return render(request, "home.html", {})


@app.get("/users/")
def users_list_view():
    q = User.objects.all().limit(10)
    return list(q)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

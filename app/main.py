import uvicorn
from fastapi import FastAPI
from app.core import (
    db
    # config
)
from cassandra.cqlengine.management import sync_table
from app.users.models import User

DB_SESSION = None

app = FastAPI()
# settings = config.get_settings()


@app.on_event("startup")
def on_startup():
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

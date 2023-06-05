from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from pydantic import BaseModel
from .config import settings
from .db import create_db_and_tables
from .router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


description = """
FastPush for faster push notifications. 🚀

Supports Push API for Progressive Web App

"""

app = FastAPI(
    lifespan=lifespan,
    title="FastPush",
    description=description,
    version="1.1",
    contact={
        "name": "Muhammad Nizamuddin Aulia",
        "url": "https://github.com/mavic111",
        "email": "muhammadnizamuddinaulia@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://www.mit.edu/~amini/LICENSE.md",
    },
    docs_url="/api/docs",
)


origins = [settings.CORS_HOSTNAME]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Metadata(BaseModel):
    name: str
    docs: str


@app.get("/", response_model=Metadata)
async def root():
    return {"name": "FastPush", "docs": "api/docs"}


app.include_router(router, prefix="/api")

from dotenv.main import load_dotenv

load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import v1_router
from db import create_db_and_tables
import os

description = """
FastPush for faster push notifications. 🚀

Supports Push API for Progressive Web App

"""

app = FastAPI(
    title="FastPush",
    description=description,
    version="1.0",
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

origins = [os.getenv("HOST", "")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    print("ayeee")
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "FastPush", "docs": "api/docs"}


app.include_router(v1_router, prefix="/api/v1")

from fastapi import APIRouter
from . import broadcast, subscription, content

v1_router = APIRouter()

v1_router.include_router(subscription.router, tags=["subscription"])
v1_router.include_router(broadcast.router, tags=["broadcast"])
v1_router.include_router(content.router, tags=["content"])

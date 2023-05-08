from fastapi import APIRouter
from . import broadcast, subscription

v1_router = APIRouter()

v1_router.include_router(subscription.router, tags=["subscription"])
v1_router.include_router(broadcast.router, tags=["broadcast"])

from fastapi import APIRouter
from .api import broadcast, subscriptions, notifications

router = APIRouter()

router.include_router(subscriptions.router, tags=["subscription"])
router.include_router(broadcast.router, tags=["broadcast"])
router.include_router(notifications.router, tags=["notification"])

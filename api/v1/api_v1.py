from fastapi import APIRouter
from . import broadcast, subscription

router = APIRouter()

router.include_router(
    subscription.router, prefix="/subscription", tags=["subscription"]
)
router.include_router(broadcast.router, prefix="/broadcast", tags=["broadcast"])

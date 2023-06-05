from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from ..config import settings
from ..models import (
    Subscription,
    NotificationCreate,
)
from ..db import get_session
from pywebpush import webpush, WebPushException
from pydantic import BaseModel, ValidationError


class BroadcastResponse(BaseModel):
    message: str


router = APIRouter()


def push_notification(
    subscription: Subscription, notification: NotificationCreate, db: Session
):
    try:
        print("Send push notification to: ", subscription.endpoint)
        webpush(
            subscription_info=subscription.dict(),
            data=notification.json(),
            vapid_private_key=settings.VAPID_PRIVATE_KEY,
            vapid_claims={"sub": "mailto:" + settings.EMAIL_ADDRESS},
        )
        return True
    except WebPushException as ex:
        print("Web Push Error: {}", repr(ex))
        if ex.response.status_code == 410:
            # Delete subscription from db
            print(f"Deleting subscription with id {subscription.id} from DB")
            print(subscription)
            try:
                statement = select(Subscription).where(
                    Subscription.id == subscription.id
                )
                results = db.exec(statement)
                expired_db_subscription = results.one()
                db.delete(expired_db_subscription)
                db.commit()
            except NoResultFound:
                print("Subscription not found or already deleted.")
            except MultipleResultsFound:
                # Result maybe more than one because endpoint is not unique (bug)
                statement = select(Subscription).where(
                    Subscription.id == subscription.id
                )
                results = db.exec(statement)
                expired_db_subscription = results.first()
                while expired_db_subscription is not None:
                    db.delete(expired_db_subscription)
                    results = db.exec(statement)
                    expired_db_subscription = results.first()
                db.commit()
        return False


@router.post("/broadcast", response_model=BroadcastResponse, status_code=202)
async def send_broadcast(
    *,
    db: Session = Depends(get_session),
    notification: NotificationCreate,
    background_tasks: BackgroundTasks,
):
    try:
        statement = select(Subscription)
        results = db.exec(statement)
        for subscription in results:
            background_tasks.add_task(push_notification, subscription, notification, db)
        return {"message": "Broadcast executed"}
    except ValidationError:
        raise HTTPException(status_code=422, detail="ValidationError")

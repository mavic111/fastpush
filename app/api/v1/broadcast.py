from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from ...config import settings
from ...models import (
    PushSubscription,
    PushSubscriptionOriginal,
    PushContent,
    PushContentCreate,
    PushContentRead,
)
from ...db import get_session
from pywebpush import webpush, WebPushException
from pydantic import ValidationError


router = APIRouter()


def push_notification(
    subscription: PushSubscription, data: PushContentCreate, db: Session
):
    try:
        subscription_push = PushSubscriptionOriginal(
            endpoint=subscription.endpoint,
            expirationTime=subscription.expirationTime,
            keys=subscription.keys_dict,
        )
        print(f"Sending web push to {subscription_push.endpoint}")
        webpush(
            subscription_info=subscription_push.dict(),
            data=data.json(),
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
                statement = select(PushSubscription).where(
                    PushSubscription.id == subscription.id
                )
                results = db.exec(statement)
                expired_db_subscription = results.one()
                db.delete(expired_db_subscription)
                db.commit()
            except NoResultFound:
                print("Subscription not found or already deleted.")
        return False


@router.post("/broadcast", status_code=202, response_model=PushContentRead)
async def broadcast(
    *,
    db: Session = Depends(get_session),
    push_content: PushContentCreate,
    background_tasks: BackgroundTasks,
):
    try:
        db_push_content = PushContent.from_orm(push_content)
        db.add(db_push_content)
        db.commit()
        db.refresh(db_push_content)
        statement = select(PushSubscription)
        results = db.exec(statement)
        for subscription in results:
            background_tasks.add_task(push_notification, subscription, push_content, db)
        return db_push_content
    except ValidationError:
        raise HTTPException(status_code=422, detail="ValidationError")

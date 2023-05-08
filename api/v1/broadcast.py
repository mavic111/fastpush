from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session, select
from pywebpush import webpush, WebPushException
from db import get_session
import os
from models import PushSubscription, PushContent, PushContentCreate, PushContentRead
from pydantic import ValidationError

router = APIRouter()


def push_notification(subscription: PushSubscription, data: PushContentCreate):
    try:
        # Removes id and serialize "keys" key
        del subscription.id
        subscription.keys = subscription.keys_dict
        webpush(
            subscription_info=subscription.dict(),
            data=data.json(),
            vapid_private_key=os.getenv("VAPID_PRIVATE_KEY", ""),
            vapid_claims={"sub": "mailto:" + os.getenv("EMAIL_ADDRESS", "")},
        )
        return True
    except WebPushException as ex:
        print("Web Push Error: {}", repr(ex))
        # Mozilla returns additional information in the body of the response.
        if ex.response and ex.response.json():
            extra = ex.response.json()
            print(
                "Remote service replied with a {}:{}, {}",
                extra.code,
                extra.errno,
                extra.message,
            )
        return False


@router.post("/", status_code=202, response_model=PushContentRead)
async def broadcast(
    *,
    db: Session = Depends(get_session),
    push_content: PushContentCreate,
    background_tasks: BackgroundTasks
):
    try:
        db_push_content = PushContent.from_orm(push_content)
        db.add(db_push_content)
        db.commit()
        db.refresh(db_push_content)
        statement = select(PushSubscription)
        results = db.exec(statement)
        for subscription in results:
            background_tasks.add_task(push_notification, subscription, push_content)
        return db_push_content
    except ValidationError:
        raise HTTPException(status_code=422, detail="ValidationError")

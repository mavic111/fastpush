from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from pydantic import ValidationError
from db import get_session
from models import (
    PushSubscriptionOriginal,
    PushSubscription,
    PushSubscriptionCreate,
    PushSubscriptionRead,
)

import json

router = APIRouter()


@router.post("/subscription", response_model=PushSubscriptionRead, status_code=201)
async def create_subscription(
    *,
    db: Session = Depends(get_session),
    subscription: PushSubscriptionOriginal,
    response: Response
):
    try:
        key_in_string = json.dumps(subscription.keys.dict())
        new_subscription = PushSubscriptionCreate(
            endpoint=subscription.endpoint,
            expirationTime=subscription.expirationTime,
            keys=key_in_string,
        )
        db_subscription = PushSubscription.from_orm(new_subscription)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription
    except ValidationError:
        raise HTTPException(status_code=422, detail="ValidationError")
    except IntegrityError:
        db.rollback()
        statement = select(PushSubscription).where(
            PushSubscription.endpoint == db_subscription.endpoint
        )
        exist_db_subscription = db.exec(statement)
        response.status_code = status.HTTP_302_FOUND
        return exist_db_subscription


@router.delete("/subscription", status_code=204)
async def delete_subscription(
    *, db: Session = Depends(get_session), subscription: dict
):
    try:
        query_subscription = PushSubscriptionCreate(
            endpoint=subscription["endpoint"],
            expirationTime=subscription["expirationTime"],
            keys=str(subscription["keys"]),
        )
        statement = select(PushSubscription).where(
            PushSubscription.endpoint == query_subscription.endpoint
        )
        results = db.exec(statement)
        db_subscription = results.one()
        db.delete(db_subscription)
        db.commit()
        # Double check
        # results = db.exec(statement)
        # subscription = results.first()
        # if subscription is not None:
        #    db.delete(subscription)
        return None
    except ValidationError:
        raise HTTPException(status_code=400, detail="ValidationError")
    except NoResultFound:
        return None

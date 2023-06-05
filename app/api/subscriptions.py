from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlmodel import Session, desc, select
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from pydantic import ValidationError
from ..db import get_session
from ..models import (
    Subscription,
    SubscriptionCreate,
    SubscriptionRead,
)

router = APIRouter()


@router.post("/subscriptions", response_model=SubscriptionRead, status_code=201)
async def create_subscription(
    *,
    db: Session = Depends(get_session),
    subscription: SubscriptionCreate,
    response: Response,
):
    try:
        db_subscription = Subscription.from_orm(subscription)
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=422, detail="ValidationError")
    except IntegrityError:
        # unused, when endpoint is unique, it raise error 'RMKeyView' object is not callable not IntegrityError
        db.rollback()
        statement = select(Subscription).where(
            Subscription.endpoint == db_subscription.endpoint
        )
        exist_db_subscription = db.exec(statement)
        response.status_code = status.HTTP_302_FOUND
        return exist_db_subscription


@router.get("/subscriptions", response_model=list[SubscriptionRead], status_code=200)
async def read_subscriptions(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    sort: Literal["asc", "desc"] = "asc",
):
    statement = (
        select(Subscription)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Subscription.id) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_subscriptions = results.fetchall()
    return db_subscriptions


@router.delete("/subscriptions", status_code=204)
async def delete_subscription(*, db: Session = Depends(get_session), endpoint: str):
    try:
        statement = select(Subscription).where(Subscription.endpoint == endpoint)
        results = db.exec(statement)
        db_subscription = results.one()
        db.delete(db_subscription)
        db.commit()
        return None
    except ValidationError:
        raise HTTPException(status_code=400, detail="ValidationError")
    except NoResultFound:
        return None
    except MultipleResultsFound:
        # result maybe more than one, because endpoint is not unique (bug)
        statement = select(Subscription).where(Subscription.endpoint == endpoint)
        results = db.exec(statement)
        db_subscription = results.first()
        while db_subscription is not None:
            db.delete(db_subscription)
            results = db.exec(statement)
            db_subscription = results.first()
        db.commit()
        return None

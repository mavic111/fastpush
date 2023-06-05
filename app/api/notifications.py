from datetime import date, datetime, timedelta
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from sqlmodel import Session, select, desc
from sqlalchemy.exc import NoResultFound
from ..db import get_session
from ..models import Notification, NotificationRead, NotificationCreate


router = APIRouter()


@router.post("/notifications", response_model=NotificationRead, status_code=201)
async def create_notification(
    *,
    db: Session = Depends(get_session),
    notification: NotificationCreate,
):
    try:
        db_notification = Notification.from_orm(notification)
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except ValidationError:
        raise HTTPException(status_code=422, detail="ValidationError")


@router.get("/notifications", response_model=list[NotificationRead], status_code=200)
async def read_notifications(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    sort: Literal["asc", "desc"] = "asc",
):
    statement = (
        select(Notification)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Notification.id) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_notifications = results.fetchall()
    return db_notifications


@router.delete("/notifications", status_code=204)
async def delete_notification(*, db: Session = Depends(get_session), id: int):
    try:
        statement = select(Notification).where(Notification.id == id)
        results = db.exec(statement)
        db_notification = results.one()
        db.delete(db_notification)
        db.commit()
        return None
    except ValidationError:
        raise HTTPException(status_code=400, detail="ValidationError")
    except NoResultFound:
        return None


@router.get(
    "/notification/today", response_model=list[NotificationRead], status_code=200
)
async def read_today_notifications(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    sort: Literal["asc", "desc"] = "asc",
):
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())
    statement = (
        select(Notification)
        .where(Notification.created_at >= start_of_day)
        .where(Notification.created_at <= end_of_day)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Notification.id) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_notifications = results.fetchall()
    return db_notifications


@router.get(
    "/notification/thisweek", response_model=list[NotificationRead], status_code=200
)
async def read_this_week_notifications(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    sort: Literal["asc", "desc"] = "asc",
):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_of_week_datetime = datetime.combine(start_of_week, datetime.min.time())
    end_of_week_datetime = datetime.combine(end_of_week, datetime.max.time())
    statement = (
        select(Notification)
        .where(Notification.created_at >= start_of_week_datetime)
        .where(Notification.created_at <= end_of_week_datetime)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Notification.created_at) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_notifications = results.fetchall()
    return db_notifications


@router.get(
    "/notification/thismonth", response_model=list[NotificationRead], status_code=200
)
async def read_this_month_notifications(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    sort: Literal["asc", "desc"] = "asc",
):
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    end_of_month = date(today.year, today.month + 1, 1) - timedelta(days=1)
    start_of_month_datetime = datetime.combine(start_of_month, datetime.min.time())
    end_of_month_datetime = datetime.combine(end_of_month, datetime.max.time())
    statement = (
        select(Notification)
        .where(Notification.created_at >= start_of_month_datetime)
        .where(Notification.created_at <= end_of_month_datetime)
        .offset(offset)
        .limit(limit)
        .order_by(desc(Notification.created_at) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_notifications = results.fetchall()
    return db_notifications

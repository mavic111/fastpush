from datetime import date, datetime, timedelta
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from sqlmodel import Session, select, desc
from ...db import get_session
from ...models import PushContent, PushContentRead, PushContentCreate


router = APIRouter()


@router.post("/content", response_model=PushContentRead, status_code=201)
async def create_content(
    *,
    db: Session = Depends(get_session),
    content: PushContentCreate,
):
    try:
        db_content = PushContent.from_orm(content)
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content
    except ValidationError:
        raise HTTPException(status_code=422, detail="ValidationError")


@router.get("/content", response_model=list[PushContentRead], status_code=200)
async def read_contents(
    *,
    db: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    sort: Literal["asc", "desc"] = "asc",
):
    statement = (
        select(PushContent)
        .offset(offset)
        .limit(limit)
        .order_by(desc(PushContent.id) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_contents = results.fetchall()
    return db_contents


@router.get("/content/today", response_model=list[PushContentRead], status_code=200)
async def read_today_contents(
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
        select(PushContent)
        .where(PushContent.created_at >= start_of_day)
        .where(PushContent.created_at <= end_of_day)
        .offset(offset)
        .limit(limit)
        .order_by(desc(PushContent.id) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_contents = results.fetchall()
    return db_contents


@router.get("/content/thisweek", response_model=list[PushContentRead], status_code=200)
async def read_this_week_contents(
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
        select(PushContent)
        .where(PushContent.created_at >= start_of_week_datetime)
        .where(PushContent.created_at <= end_of_week_datetime)
        .offset(offset)
        .limit(limit)
        .order_by(desc(PushContent.created_at) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_contents = results.fetchall()
    return db_contents


@router.get("/content/thismonth", response_model=list[PushContentRead], status_code=200)
async def read_this_month_contents(
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
        select(PushContent)
        .where(PushContent.created_at >= start_of_month_datetime)
        .where(PushContent.created_at <= end_of_month_datetime)
        .offset(offset)
        .limit(limit)
        .order_by(desc(PushContent.created_at) if sort == "desc" else None)
    )
    results = db.exec(statement)
    db_contents = results.fetchall()
    return db_contents

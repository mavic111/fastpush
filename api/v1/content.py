from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import ValidationError
from sqlmodel import Session, select, desc
from db import get_session
from models import PushContent, PushContentRead, PushContentCreate


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

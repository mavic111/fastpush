from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class PushContentBase(SQLModel):
    title: str
    message: str
    url: Optional[str] = "/"


class PushContent(PushContentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)


class PushContentCreate(PushContentBase):
    pass


class PushContentRead(PushContentBase):
    id: int
    created_at: datetime


class PushContentUpdate(SQLModel):
    title: Optional[str] = None
    message: Optional[str] = None
    url: Optional[str] = "/"

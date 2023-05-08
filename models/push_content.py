from typing import Optional
from sqlmodel import SQLModel, Field


class PushContentBase(SQLModel):
    title: str
    message: str


class PushContent(PushContentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class PushContentCreate(PushContentBase):
    pass


class PushContentRead(PushContentBase):
    id: int


class PushContentUpdate(SQLModel):
    title: Optional[str] = None
    message: Optional[str] = None

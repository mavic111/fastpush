from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class NotificationBase(SQLModel):
    title: str
    body: str
    url: str


class Notification(NotificationBase, table=True):
    __tablename__ = "notifications"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)


class NotificationCreate(NotificationBase):
    pass


class NotificationRead(NotificationBase):
    id: int
    created_at: datetime


class NotificationUpdate(SQLModel):
    title: Optional[str]
    body: Optional[str]
    url: Optional[str]

from datetime import datetime
from typing import Optional
from pydantic import validator
from sqlmodel import Column, SQLModel, Field, JSON


class KeysField(SQLModel, table=False):
    auth: str
    p256dh: str


class SubscriptionBase(SQLModel):
    endpoint: str
    expiration_time: Optional[int]
    keys: KeysField


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionRead(SubscriptionBase):
    id: int
    created_at: datetime


class SubscriptionUpdate(SQLModel):
    endpoint: Optional[str]
    expiration_time: Optional[int]
    keys: Optional[KeysField]


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"
    id: Optional[int] = Field(default=None, primary_key=True)
    endpoint: str = Field(nullable=False, unique=True)
    expiration_time: Optional[int] = Field(default=None)
    keys: KeysField = Field(sa_column=Column(JSON), nullable=False)
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    @validator("keys")
    def val_complex(cls, val: KeysField):
        # Used in order to store pydantic models as dicts
        return val.dict()

    class Config:
        arbitrary_types_allowed = True

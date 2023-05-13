from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import types
import json


class Keys(SQLModel):
    auth: str
    p256dh: str


class PushSubscriptionOriginal(SQLModel):
    endpoint: str
    expirationTime: Optional[int] = None
    keys: Keys


class PushSubscriptionBase(SQLModel):
    endpoint: str
    expirationTime: Optional[int] = None
    keys: str


class PushSubscriptionCreate(PushSubscriptionBase):
    pass


class PushSubscriptionRead(PushSubscriptionBase):
    id: int
    created_at: datetime


class PushSubscriptionUpdate(SQLModel):
    endpoint: Optional[str] = None
    expirationTime: Optional[int] = None
    keys: Optional[str] = None


class PushSubscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    endpoint: str = Field(unique=True)
    expirationTime: Optional[int] = None
    keys: str = Field(sa_column=types.NVARCHAR(length=500))
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)

    @property
    def keys_dict(self):
        return json.loads(self.keys)

    @keys_dict.setter
    def keys_dict(self, value):
        self.keys = json.dumps(value)

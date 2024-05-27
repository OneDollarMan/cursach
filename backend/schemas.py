import uuid
from datetime import datetime
from typing import List, Optional

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict


class UserRead(schemas.BaseUser[uuid.UUID]):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    passport: str
    description: Optional[str]


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    passport: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    passport: str
    description: str


class SubscriptionLevelRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author_id: uuid.UUID
    is_chat_available: bool


class UserReadSubscriptionLevels(schemas.BaseUser[uuid.UUID]):
    model_config = ConfigDict(from_attributes=True)
    first_name: str
    last_name: str
    passport: str
    description: Optional[str]
    subscription_levels: List[SubscriptionLevelRead]


class SubscriptionLevelCreate(BaseModel):
    title: str
    is_chat_available: bool


class SubscriptionLevelUpdate(BaseModel):
    title: str
    is_chat_available: bool


class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    subscriber: UserRead
    author: UserRead
    subscription_level: SubscriptionLevelRead


class SubscriptionCreate(BaseModel):
    author_id: uuid.UUID
    subscription_level_id: int


class SubscriptionUpdate(BaseModel):
    author_id: uuid.UUID
    subscription_level_id: int


class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    created_by: uuid.UUID
    created_at: datetime
    subscription_level_id: int
    author: UserRead
    subscription_level: SubscriptionLevelRead


class ArticleCreate(BaseModel):
    title: str
    content: str
    subscription_level_id: int


class ArticleUpdate(BaseModel):
    title: str
    content: str
    subscription_level_id: int


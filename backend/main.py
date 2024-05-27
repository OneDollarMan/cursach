import uuid
from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from user_manager import auth_backend, fastapi_users, current_active_user
from db import create_db_and_tables, get_async_session
from models import User
import service, schemas

app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/api/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(schemas.UserRead, schemas.UserCreate),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(schemas.UserRead),
    prefix="/api/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(schemas.UserReadSubscriptionLevels, schemas.UserUpdate),
    prefix="/api/users",
    tags=["users"],
)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


@app.get('/api/users', response_model=List[schemas.UserReadSubscriptionLevels], tags=['users'])
async def explore(user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_all_users(s)


@app.get('/api/author_info/{id}', response_model=schemas.UserReadSubscriptionLevels, tags=['users'])
async def explore(id: uuid.UUID, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_author_info(id, user, s)


@app.get('/api/subscriptions', response_model=List[schemas.SubscriptionRead], tags=['subscriptions'])
async def explore(user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_user_subscriptions(user, s)


@app.post("/api/subscribe", response_model=schemas.SubscriptionRead, tags=['subscriptions'])
async def post_subscribe(subscription: schemas.SubscriptionCreate, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.subscribe(subscription, user, s)


@app.post("/api/unsubscribe/{author_id}", tags=['subscriptions'])
async def post_unsubscribe(author_id: uuid.UUID, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.unsubscribe(author_id, user, s)


@app.get("/api/subscription_levels", response_model=List[schemas.SubscriptionLevelRead], tags=['subscription_levels'])
async def get_subscription_levels(user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_all_subscription_levels(s)


@app.post("/api/subscription_levels", response_model=schemas.SubscriptionLevelRead, tags=['subscription_levels'])
async def create_subscription_level(subscription_level: schemas.SubscriptionLevelCreate, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.create_subscription_level(subscription_level, user, s)


@app.get("/api/subscription_levels/{id}", response_model=schemas.SubscriptionLevelRead, tags=['subscription_levels'])
async def get_subscription_level(id: int, s: AsyncSession = Depends(get_async_session)):
    return await service.get_subscription_level(id, s)


@app.patch("/api/subscription_levels/{id}", response_model=schemas.SubscriptionLevelRead, tags=['subscription_levels'])
async def patch_subscription_level(id: int, subscription_level: schemas.SubscriptionLevelUpdate, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.update_subscription_level(id, subscription_level, user, s)


@app.delete("/api/subscription_levels/{id}", tags=['subscription_levels'])
async def delete_subscription_level(id: int, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.delete_subscription_level(id, user, s)


@app.get("/api/articles", response_model=List[schemas.ArticleRead], tags=['articles'])
async def get_articles(user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_all_articles(s)


@app.get("/api/user_articles", response_model=List[schemas.ArticleRead], tags=['articles'])
async def get_user_articles(user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_user_articles(user, s)


@app.get("/api/author_articles", response_model=List[schemas.ArticleRead], tags=['articles'])
async def get_all_authors_articles(user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_all_authors_articles(user, s)


@app.get("/api/author_articles/{author_id}", response_model=List[schemas.ArticleRead], tags=['articles'])
async def get_author_articles(author_id: uuid.UUID, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_author_articles(author_id, user, s)


@app.post("/api/articles", response_model=schemas.ArticleRead, tags=['articles'])
async def create_article(article: schemas.ArticleCreate, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.create_article(article, user, s)


@app.get("/api/articles/{id}", response_model=schemas.ArticleRead, tags=['articles'])
async def get_article(id: int, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.get_article(id, s)


@app.patch("/api/articles/{id}", response_model=schemas.ArticleRead, tags=['articles'])
async def patch_article(id: int, article: schemas.ArticleUpdate, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.update_article(id, article, user, s)


@app.delete("/api/articles/{id}", tags=['articles'])
async def delete_article(id: int, user: User = Depends(current_active_user), s: AsyncSession = Depends(get_async_session)):
    return await service.delete_article(id, user, s)

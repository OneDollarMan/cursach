import uuid

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
import schemas, models


async def get_all_users(s: AsyncSession):
    users = await s.execute(select(models.User))
    res = []
    for user in users:
        res.append(user[0])
    return res


async def get_author_info(author_id: uuid.UUID, user: models.User, s: AsyncSession):
    subscription = await s.execute(select(models.Subscription).where(models.Subscription.author_id == author_id).where(models.Subscription.subscriber_id == user.id))
    if subscription is None:
        raise HTTPException(status_code=400, detail="User doesn't subscribed to author")

    user = await s.get(models.User, author_id)
    return user


async def get_user_subscriptions(user: models.User, s: AsyncSession):
    res = []
    subs = await s.execute(select(models.Subscription).where(models.Subscription.subscriber_id == user.id))
    for sub in subs:
        res.append(sub[0])
    return res


async def get_user_articles(user: models.User, s: AsyncSession):
    res = []
    articles = await s.execute(select(models.Article).where(models.Article.created_by == user.id))
    for article in articles:
        res.append(article[0])
    return res


async def get_all_subscription_levels(s: AsyncSession):
    return await s.execute(select(models.SubscriptionLevel))


async def create_subscription_level(subscription_level: schemas.SubscriptionLevelCreate, user: models.User, s: AsyncSession):
    sl = models.SubscriptionLevel(title=subscription_level.title, is_chat_available=subscription_level.is_chat_available, author_id=user.id)
    s.add(sl)
    await s.commit()
    await s.refresh(sl)
    return sl


async def get_subscription_level(id: int, s: AsyncSession):
    return await s.get(models.SubscriptionLevel, id)


async def update_subscription_level(id: int, subscription_level: schemas.SubscriptionLevelUpdate, user: models.User, s: AsyncSession):
    sl = await s.get(models.SubscriptionLevel, id)
    if sl.author_id != user.id:
        raise HTTPException(status_code=400, detail="Subscription level doesn't belong to user")

    sl.title = subscription_level.title
    sl.is_chat_available = subscription_level.content
    s.add(sl)
    await s.commit()
    await s.refresh(sl)
    return sl


async def delete_subscription_level(id: int, user: models.User, s: AsyncSession):
    sl = await s.get(models.SubscriptionLevel, id)
    if sl.author_id != user.id:
        raise HTTPException(status_code=400, detail="Subscription level doesn't belong to user")

    await s.execute(delete(models.Article).where(models.Article.subscription_level_id == id))
    await s.execute(delete(models.Subscription).where(models.Subscription.subscription_level_id == id))
    await s.delete(sl)
    await s.commit()
    return True


async def subscribe(subscription: schemas.SubscriptionCreate, user: models.User, s: AsyncSession):
    sub = (await s.execute(select(models.Subscription).where(models.Subscription.subscriber_id == user.id).where(models.Subscription.author_id == subscription.author_id))).first()

    author = await s.get(models.User, subscription.author_id)
    if author is None:
        raise HTTPException(status_code=400, detail="Author doesn't exists")

    sl = await s.get(models.SubscriptionLevel, subscription.subscription_level_id)
    if sl is None:
        raise HTTPException(status_code=400, detail="Subscription level doesn't exists")

    if sl.author_id != author.id:
        raise HTTPException(status_code=400, detail="Subscription level doesn't belong to author")

    if sub is None:
        sub = models.Subscription(subscriber_id=user.id, author_id=author.id, subscription_level_id=sl.id)
    else:
        sub = sub[0]
        sub.subscription_level_id = sl.id
    s.add(sub)
    await s.commit()
    await s.refresh(sub)
    return sub


async def unsubscribe(author_id: uuid.UUID, user: models.User, s: AsyncSession):
    subscription = await s.execute(select(models.Subscription).where(models.Subscription.author_id == author_id).where(
        models.Subscription.subscriber_id == user.id))
    if subscription is None:
        raise HTTPException(status_code=400, detail="User doesn't subscribed to author")

    await s.delete(subscription.fetchone()[0])
    await s.commit()
    return True


async def get_all_articles(s: AsyncSession):
    return await s.execute(select(models.Article))


async def get_all_authors_articles(user: models.User, s: AsyncSession):
    res = []
    subscriptions = await s.execute(select(models.Subscription).where(models.Subscription.subscriber_id == user.id))
    for subscription in subscriptions:
        articles = await s.execute(select(models.Article).where(models.Article.subscription_level_id == subscription[0].subscription_level_id))
        for article in articles:
            res.append(article[0])
    return res


async def get_author_articles(author_id: uuid.UUID, user: models.User, s: AsyncSession):
    subscription = await s.execute(select(models.Subscription).where(models.Subscription.author_id == author_id).where(models.Subscription.subscriber_id == user.id))
    if subscription is None:
        raise HTTPException(status_code=400, detail="User doesn't subscribed to author")
    subscription = subscription.fetchone()[0]
    articles = await s.execute(select(models.Article).where(models.Article.subscription_level_id == subscription.subscription_level_id))
    res = []
    for article in articles:
        res.append(article[0])
    return res


async def create_article(article: schemas.ArticleCreate, user: models.User, s: AsyncSession):
    subscription_level = await s.get(models.SubscriptionLevel, article.subscription_level_id)
    if subscription_level.author_id != user.id:
        raise HTTPException(status_code=400, detail="Subscription level doesn't belong to user")

    a = models.Article(title=article.title, content=article.content, created_by=user.id, subscription_level_id=article.subscription_level_id)
    s.add(a)
    await s.commit()
    await s.refresh(a)
    return a


async def get_article(id: int, s: AsyncSession):
    return await s.get(models.Article, id)


async def update_article(id: int, article: schemas.ArticleUpdate, user: models.User, s: AsyncSession):
    a = await s.get(models.Article, id)
    if a.created_by != user.id:
        raise HTTPException(status_code=400, detail="Article doesn't belong to user")

    a.title = article.title
    a.content = article.content
    a.subscription_level_id = article.subscription_level_id
    s.add(a)
    await s.commit()
    await s.refresh(a)
    return a


async def delete_article(id: int, user: models.User, s: AsyncSession):
    a = await s.get(models.Article, id)
    if a.created_by != user.id:
        raise HTTPException(status_code=400, detail="Article doesn't belong to user")

    await s.delete(a)
    await s.commit()
    return True

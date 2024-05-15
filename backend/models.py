from sqlalchemy import Column, Integer, String, UUID, Boolean, ForeignKey, func, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID


class Base(DeclarativeBase):
    ...


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    subscription_levels = relationship('SubscriptionLevel', back_populates='author', lazy='selectin')
    #subscriptions = relationship('Subscription', back_populates='subscriber', lazy='selectin')
    #subscribers = relationship('Subscription', back_populates='author', lazy='selectin')
    articles = relationship('Article', back_populates='author', lazy='selectin')


class SubscriptionLevel(Base):
    __tablename__ = 'subscription_levels'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    is_chat_available = Column(Boolean, nullable=False)

    author = relationship('User', back_populates='subscription_levels', lazy='joined')
    subscriptions = relationship('Subscription', back_populates='subscription_level', lazy='joined')
    articles = relationship("Article", back_populates='subscription_level', lazy='selectin')


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    subscriber_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    subscription_level_id = Column(Integer, ForeignKey('subscription_levels.id'), nullable=False)

    subscriber = relationship('User', foreign_keys=[subscriber_id], lazy='selectin')
    author = relationship('User', foreign_keys=[author_id], lazy='selectin')
    subscription_level = relationship('SubscriptionLevel', back_populates='subscriptions', lazy='selectin')


class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    subscription_level_id = Column(Integer, ForeignKey('subscription_levels.id'), nullable=False)

    author = relationship('User', back_populates='articles', lazy='selectin')
    subscription_level = relationship('SubscriptionLevel', back_populates='articles', lazy='selectin')


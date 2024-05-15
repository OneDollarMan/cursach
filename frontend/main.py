import logging
import service
from fastapi import Request, Cookie, FastAPI
from typing import Annotated
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

app = FastAPI(docs_url="/docs")
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse('landing.html', {'request': request})


@app.get('/explore')
async def explore(request: Request, fastapiusersauth: Annotated[str | None, Cookie()] = None):
    user = service.get_user(fastapiusersauth)
    authors = service.get_users(fastapiusersauth)
    return templates.TemplateResponse('explore.html', {'request': request, 'user': user, 'users': authors})


@app.get('/profile')
async def profile(request: Request, fastapiusersauth: Annotated[str | None, Cookie()] = None):
    user = service.get_user(fastapiusersauth)
    return templates.TemplateResponse('profile.html', {'request': request, 'user': user})


@app.get('/profile/{id}')
async def profile_id(request: Request, id: int, fastapiusersauth: Annotated[str | None, Cookie()] = None):
    return templates.TemplateResponse('profile.html', {'request': request})


@app.get('/subscriptions')
async def subscriptions(request: Request, fastapiusersauth: Annotated[str | None, Cookie()] = None):
    user = service.get_user(fastapiusersauth)
    subscriptions = service.get_user_subscriptions(fastapiusersauth)
    return templates.TemplateResponse('subscriptions.html', {'request': request, 'user': user, 'subscriptions': subscriptions})


@app.get('/feed')
async def feed(request: Request, fastapiusersauth: Annotated[str | None, Cookie()] = None):
    user = service.get_user(fastapiusersauth)
    return templates.TemplateResponse('feed.html', {'request': request, 'user': user})


@app.get('/articles')
async def articles(request: Request, fastapiusersauth: Annotated[str | None, Cookie()] = None):
    user = service.get_user(fastapiusersauth)
    articles = service.get_user_articles(fastapiusersauth)
    return templates.TemplateResponse('articles.html', {'request': request, 'user': user, 'articles': articles})

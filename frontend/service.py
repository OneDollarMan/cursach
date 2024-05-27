import requests
from fastapi import HTTPException
from datetime import datetime

url = 'http://backend:8000'


def format_date(string:str) -> str:
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%f").strftime("%d %b %Y, %H:%S")


def get_user(token):
    user = requests.get(url=f'{url}/api/users/me', cookies={'fastapiusersauth': token})
    if user.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    return user.json()


def get_author_info(token, id):
    user = requests.get(url=f'{url}/api/author_info/{id}', cookies={'fastapiusersauth': token})
    if user.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    return user.json()


def get_users(token):
    users = requests.get(url=f'{url}/api/users', cookies={'fastapiusersauth': token})
    if users.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    return users.json()


def get_user_subscriptions(token):
    subscriptions = requests.get(url=f'{url}/api/subscriptions', cookies={'fastapiusersauth': token})
    if subscriptions.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    return subscriptions.json()


def get_user_articles(token):
    articles = requests.get(url=f'{url}/api/user_articles', cookies={'fastapiusersauth': token})
    if articles.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    res = articles.json()
    for article in res:
        article['created_at'] = format_date(article['created_at'])
    return res


def get_author_articles(token, author_id):
    articles = requests.get(url=f'{url}/api/author_articles/{author_id}', cookies={'fastapiusersauth': token})
    if articles.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    res = articles.json()
    for article in res:
        article['created_at'] = format_date(article['created_at'])
    return res


def get_all_authors_articles(token):
    articles = requests.get(url=f'{url}/api/author_articles/', cookies={'fastapiusersauth': token})
    if articles.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    res = articles.json()
    for article in res:
        article['created_at'] = format_date(article['created_at'])
    return res

import requests
from fastapi import HTTPException


url = 'http://backend:8000'


def get_user(token):
    user = requests.get(url=f'{url}/api/users/me', cookies={'fastapiusersauth': token})
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
    subscriptions = requests.get(url=f'{url}/api/user_articles', cookies={'fastapiusersauth': token})
    if subscriptions.status_code != 200:
        raise HTTPException(status_code=400, detail="Access denied")
    return subscriptions.json()

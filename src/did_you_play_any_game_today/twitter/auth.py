from requests_oauthlib import OAuth1Session

from ..config import settings


def auth() -> OAuth1Session:
    consumer_key = settings.consumer_key
    consumer_secret = settings.consumer_secret

    access_token = settings.access_token
    access_token_secret = settings.access_token_secret

    return OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )

import collections
import typing
from re import match
from datetime import time

from dynaconf import Dynaconf, Validator  # type: ignore
from pytz import all_timezones


class Settings(collections.abc.Mapping):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
    positive_tweet: str
    negative_tweet: str
    state_file_path: str
    tweet_at: str
    tweet_at_timezone: str


validators = [
    Validator(
        'consumer_key',
        'consumer_secret',
        'access_token',
        'access_token_secret',
        must_exist=True,
        messages=dict(
            must_exist_true=(
                'Twitter APP and Oauth keys/secrets are required. '
                'Check authorize.py to generate the .secrets.json '
                'file that contains these settings.'
            )
        )
    ),
    Validator(
        'positive_tweet', default='🎊 Yes! 🎉', must_exist=True,
    ),
    Validator(
        'negative_tweet', default='No...🥲', must_exist=True,
    ),
    Validator(
        'state_file_path', default='.state.json', must_exist=True,
    ),
    Validator(
        'tweet_at',
        default='04:44',
        must_exist=True,
        # TOML parser convert local time to datetime.time instance
        # we'll want to change it back to string to use it for the schedule.
        cast=lambda v: v.strftime('%H:%M:%S') if isinstance(v, time) else v,
        # cast happens after the condition validation so the
        # `isinstance` branch is required
        condition=lambda v: isinstance(v, time) or match(
            (
                r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$'
                r'|'
                r'^([0-1][0-9]|2[0-3])(:[0-5][0-9]){2}$'
            ),
            v,
        ),
        messages=dict(
            condition='{name} must be in HH:MM or HH:MM:SS format'
        ),
    ),
    Validator(
        'tweet_at_timezone',
        default='America/Vancouver',
        must_exist=True,
        is_in=all_timezones,
        messages=dict(
            operations=(
                '{name} must be in `pytz.all_timezones` '
                'but it is {value} in env {env}'
            ),
        ),
    ),
]


settings = typing.cast(Settings, Dynaconf(
    envvar_prefix="DYPAGT",
    settings_files=[
        "settings.toml",
        "/run/secrets/.secrets.json",
        ".secrets.json"
    ],
    load_dotenv=True,
    validators=validators,
))

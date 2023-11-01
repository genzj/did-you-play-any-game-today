import collections
import typing

from dynaconf import Dynaconf  # type: ignore


class Settings(collections.abc.Mapping):
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
    positive_tweet: typing.Optional[str]
    negative_tweet: typing.Optional[str]
    state_file_path: typing.Optional[str]
    tweet_at: typing.Optional[str]
    tweet_at_timezone: typing.Optional[str]


settings = typing.cast(Settings, Dynaconf(
    envvar_prefix="DYPAGT",
    settings_files=[
        "settings.toml",
        "/run/secrets/.secrets.json",
        ".secrets.json"
    ],
    load_dotenv=True,
))

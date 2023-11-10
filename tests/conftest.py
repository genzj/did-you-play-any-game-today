import json
import tomllib
from pathlib import Path
from typing import Callable

import pytest
from fastapi.testclient import TestClient
from requests import Request

from did_you_play_any_game_today.config import Settings, settings


@pytest.fixture(scope='session')
def state_file(tmp_path_factory) -> Path:
    return tmp_path_factory.mktemp('state') / 'state.json'


@pytest.fixture(scope='session')
def config_file(tmp_path_factory, state_file) -> Path:
    config_file = tmp_path_factory.mktemp('config') / 'merged_settings.json'

    with open('test_settings.toml', 'rb') as inf:
        settings_templ = tomllib.load(inf)

    settings_templ['state_file_path'] = str(state_file)
    with open(config_file, 'w') as outf:
        json.dump(settings_templ, outf)

    return config_file


@pytest.fixture(autouse=True, scope='session')
def load_test_settings(config_file: Path) -> Settings:
    # configure() only set default values, so it cannot override the
    # settings_files as it's been set by the settings' definition
    # using include to override the configs.
    # Note that only env-var name can be used and the init kwarg alias
    # `includes` doesn't work because configure() doesn't resolve aliases
    settings.configure(  # type: ignore
        INCLUDES_FOR_DYNACONF=[str(config_file.absolute())],
    )
    assert settings.consumer_key == 'fake_consumer_key'
    assert settings.consumer_secret == 'fake_consumer_secret'
    assert settings.access_token == 'fake_access_token'
    assert settings.access_token_secret == 'fake_access_secret'
    assert settings.tweet_at == '12:34'
    assert settings.tweet_at_timezone == 'UTC'
    assert settings.state_file_path.endswith('/state.json')
    return settings


@pytest.fixture
def client():
    # this import must stay here instead of in the module scope
    # because we need the test settings to be loaded before importing the app
    from did_you_play_any_game_today.server.main import app
    return TestClient(app)


OAuthAsserter = Callable[[Request], None]


def assert_has_oauth(request: Request):
    headers = request.headers
    assert 'Authorization' in headers
    assert headers['Authorization'].startswith(b'OAuth ')
    auth = dict()
    for sec in headers['Authorization'].decode('utf-8').lstrip('OAuth ').split(', '):
        k, v = sec.split('=', 1)
        auth[k] = v
    assert 'oauth_nonce' in auth
    assert 'oauth_timestamp' in auth
    assert 'oauth_signature' in auth
    assert auth['oauth_version'] == '"1.0"'
    assert auth['oauth_signature_method'] == '"HMAC-SHA1"'
    assert auth['oauth_consumer_key'] == '"fake_consumer_key"'
    assert auth['oauth_token'] == '"fake_access_token"'


@pytest.fixture(scope='session')
def oauth_asserter() -> OAuthAsserter:
    return assert_has_oauth

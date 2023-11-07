import json
import tomllib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from did_you_play_any_game_today.config import settings


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
def load_test_settings(config_file: Path):
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


@pytest.fixture
def client():
    # this import must stay here instead of in the module scope
    # because we need the test settings to be loaded before importing the app
    from did_you_play_any_game_today.server.main import app
    return TestClient(app)

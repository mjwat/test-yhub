from typing import Dict

import pytest

from utils.config import get_env_config


@pytest.fixture(scope="session")
def env_config() -> Dict[str, str]:
    return get_env_config()


@pytest.fixture(scope="session")
def base_url(env_config: Dict[str, str]) -> str:
    return env_config["BASE_URL"].rstrip("/")

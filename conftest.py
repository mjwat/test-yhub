import logging
from typing import Dict

import pytest

from clients.auth_client import AuthClient
from utils.config import get_env_config


@pytest.fixture(scope="session", autouse=True)
def configure_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")


@pytest.fixture(scope="session")
def env_config() -> Dict[str, str]:
    return get_env_config()


@pytest.fixture(scope="session")
def api_base_url(env_config: Dict[str, str]) -> str:
    return env_config["BASE_URL"].rstrip("/")


@pytest.fixture(scope="function")
def auth_client(api_base_url: str, env_config: Dict[str, str]) -> AuthClient:
    return AuthClient(
        base_url=api_base_url,
        csrf_endpoint=env_config["CSRF_ENDPOINT"],
        login_endpoint=env_config["LOGIN_ENDPOINT"],
    )


@pytest.fixture(scope="function")
def test_user(env_config: Dict[str, str]) -> Dict[str, str]:
    return {
        "email": env_config["TEST_USER_EMAIL"],
        "password": env_config["TEST_USER_PASSWORD"],
    }

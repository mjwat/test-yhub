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
        auth_check_endpoint=env_config["AUTH_CHECK_ENDPOINT"],
    )


@pytest.fixture(scope="function")
def valid_login_payload(env_config: Dict[str, str]) -> Dict[str, str]:
    return {
        "email": env_config["TEST_USER_EMAIL"],
        "password": env_config["TEST_USER_PASSWORD"],
    }


@pytest.fixture(scope="function")
def authenticated_session(auth_client: AuthClient, valid_login_payload: Dict[str, str]) -> AuthClient:
    csrf_response = auth_client.get_csrf_cookie()
    if csrf_response.status_code not in (200, 204):
        raise RuntimeError(
            f"CSRF initialization failed. Status code: {csrf_response.status_code}. Body: {csrf_response.text}"
        )

    xsrf_token = auth_client.get_xsrf_token()
    if not xsrf_token:
        raise RuntimeError("XSRF-TOKEN cookie was not returned by /sanctum/csrf-cookie.")

    login_response = auth_client.login(
        email=valid_login_payload["email"],
        password=valid_login_payload["password"],
        xsrf_token=xsrf_token,
    )
    if login_response.status_code not in (200, 204):
        raise RuntimeError(
            f"Login failed in authenticated_session fixture. Status code: {login_response.status_code}. "
            f"Body: {login_response.text}"
        )

    return auth_client

import logging
from typing import Dict

import pytest

from clients.auth_client import AuthClient
from clients.site_client import SiteClient
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


@pytest.fixture(scope="session")
def admin_base_url(env_config: Dict[str, str]) -> str:
    return env_config["ADMIN_BASE_URL"].rstrip("/")


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


@pytest.fixture(scope="function")
def git_repo_url(env_config: Dict[str, str]) -> str:
    return env_config["GIT_REP_URL"]


@pytest.fixture(scope="function")
def authenticated_auth_client(auth_client: AuthClient, test_user: Dict[str, str]) -> AuthClient:
    response = auth_client.authenticate(
        email=test_user["email"],
        password=test_user["password"],
    )
    if response.status_code not in (200, 204):
        raise RuntimeError(
            f"Authentication failed. Status code: {response.status_code}. "
            f"URL: {response.request.url}. Body: {response.text[:500]}"
        )
    return auth_client


@pytest.fixture(scope="function")
def site_client(
    admin_base_url: str,
    env_config: Dict[str, str],
    authenticated_auth_client: AuthClient,
) -> SiteClient:
    return SiteClient(
        base_url=admin_base_url,
        site_create_page_endpoint=env_config["SITE_CREATE_PAGE_ENDPOINT"],
        site_endpoint=env_config["SITE_ENDPOINT"],
        session=authenticated_auth_client.session,
    )


@pytest.fixture(scope="function")
def ensure_no_sites(site_client: SiteClient) -> None:
    existing_sites = site_client.get_user_sites()
    if existing_sites:
        summary = site_client.delete_all_sites()
        if summary["failed_count"] > 0:
            raise RuntimeError(f"Site cleanup failed for some items: {summary}")

    remaining_sites = site_client.get_user_sites()
    if remaining_sites:
        raise RuntimeError(
            f"Site cleanup precondition failed. Expected zero sites before test, got: {remaining_sites}"
        )

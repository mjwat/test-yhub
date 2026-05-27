from typing import Dict

import pytest

from clients.auth_client import AuthClient
from clients.site_client import SiteClient


@pytest.fixture(scope="session")
def admin_base_url(env_config: Dict[str, str]) -> str:
    return env_config["ADMIN_BASE_URL"].rstrip("/")


@pytest.fixture(scope="function")
def git_repo_url(env_config: Dict[str, str]) -> str:
    return env_config["GIT_REP_URL"]


@pytest.fixture(scope="function")
def site_client(
    admin_base_url: str,
    env_config: Dict[str, str],
    logged_in_client: AuthClient,
) -> SiteClient:
    return SiteClient(
        base_url=admin_base_url,
        site_create_page_endpoint=env_config["SITE_CREATE_PAGE_ENDPOINT"],
        site_endpoint=env_config["SITE_ENDPOINT"],
        session=logged_in_client.session,
    )


@pytest.fixture(scope="function")
def clean_user_sites(site_client: SiteClient) -> None:
    existing_sites = site_client.get_user_sites()
    if existing_sites:
        cleanup_summary = site_client.delete_all_sites()
        if cleanup_summary["failed_count"] > 0:
            raise RuntimeError(f"API precondition cleanup failed for some sites: {cleanup_summary}")

    remaining_sites = site_client.get_user_sites()
    if remaining_sites:
        raise RuntimeError(
            "API precondition cleanup did not finish. "
            f"Expected zero sites before test, got: {remaining_sites}"
        )

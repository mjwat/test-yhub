from typing import Dict

import pytest

from clients.auth_client import AuthClient
from clients.site_client import SITE_COUNT_LIMIT
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
def ensure_site_creation_available(site_client: SiteClient) -> None:
    if site_client.is_site_count_limit_reached():
        cleanup_summary = site_client.delete_all_sites()
        if cleanup_summary["failed_count"] > 0:
            raise RuntimeError(f"API precondition cleanup failed for some sites: {cleanup_summary}")

    remaining_sites = site_client.get_user_sites()
    if len(remaining_sites) >= SITE_COUNT_LIMIT:
        raise RuntimeError(
            "API site-creation precondition did not finish. "
            f"Expected fewer than {SITE_COUNT_LIMIT} sites before test, got: {remaining_sites}"
        )

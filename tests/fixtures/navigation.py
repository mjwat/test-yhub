from typing import Dict

import pytest

from utils.url import build_url


@pytest.fixture(scope="session")
def login_path(env_config: Dict[str, str]) -> str:
    return env_config["LOGIN_PATH"]


@pytest.fixture(scope="session")
def dashboard_path(env_config: Dict[str, str]) -> str:
    return env_config["DASHBOARD_PATH"]


@pytest.fixture(scope="session")
def site_create_path(env_config: Dict[str, str]) -> str:
    return env_config["SITE_CREATE_PATH"]


@pytest.fixture(scope="session")
def site_create_url(admin_base_url: str, site_create_path: str) -> str:
    return build_url(admin_base_url, site_create_path)


@pytest.fixture(scope="session")
def sites_list_path(env_config: Dict[str, str]) -> str:
    return env_config["SITES_LIST_PATH"]


@pytest.fixture(scope="session")
def sites_list_url(admin_base_url: str, sites_list_path: str) -> str:
    return build_url(admin_base_url, sites_list_path)

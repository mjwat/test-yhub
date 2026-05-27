from typing import Dict

import pytest


@pytest.fixture(scope="session")
def login_path(env_config: Dict[str, str]) -> str:
    return env_config["LOGIN_PATH"]


@pytest.fixture(scope="session")
def dashboard_path(env_config: Dict[str, str]) -> str:
    return env_config["DASHBOARD_PATH"]


@pytest.fixture(scope="session")
def site_create_path(env_config: Dict[str, str]) -> str:
    configured = env_config["SITE_CREATE_PATH"]
    return configured if configured.startswith("/admin") else f"/admin{configured}"


@pytest.fixture(scope="session")
def sites_list_path(env_config: Dict[str, str]) -> str:
    configured = env_config["SITES_LIST_PATH"]
    return configured if configured.startswith("/admin") else f"/admin{configured}"

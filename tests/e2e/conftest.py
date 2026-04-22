import os
from typing import Dict

import pytest


@pytest.fixture(scope="session")
def ui_user(env_config: Dict[str, str]) -> Dict[str, str]:
    return {
        "email": env_config["TEST_USER_EMAIL"],
        "password": env_config["TEST_USER_PASSWORD"],
    }


@pytest.fixture(scope="session")
def login_path(env_config: Dict[str, str]) -> str:
    return env_config["LOGIN_PATH"]


@pytest.fixture(scope="session")
def dashboard_path(env_config: Dict[str, str]) -> str:
    return env_config["DASHBOARD_PATH"]


@pytest.fixture(scope="session")
def browser_context_args(base_url: str) -> Dict[str, object]:
    return {
        "base_url": base_url,
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture(scope="session")
def browser_type_launch_args() -> Dict[str, object]:
    headed = os.getenv("PW_HEADED", "").strip().lower() in {"1", "true", "yes", "on"}
    return {"headless": not headed}

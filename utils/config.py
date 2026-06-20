import os
from typing import Dict

from dotenv import load_dotenv


def _get_required_value(*names: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value is not None and value.strip():
            return value.strip()
    raise RuntimeError(f"Missing required environment variable. Expected one of: {', '.join(names)}")


def get_env_config() -> Dict[str, str]:
    load_dotenv()

    config: Dict[str, str] = {
        "BASE_URL": _get_required_value("BASE_URL"),
        "ADMIN_BASE_URL": _get_required_value("ADMIN_BASE_URL"),
        "TEST_USER_EMAIL": _get_required_value("TEST_USER_EMAIL"),
        "TEST_USER_PASSWORD": _get_required_value("TEST_USER_PASSWORD"),
        "GIT_REP_URL": _get_required_value("GIT_REP_URL"),
    }


    config["CSRF_ENDPOINT"] = os.getenv("CSRF_ENDPOINT", "/sanctum/csrf-cookie").strip()
    config["LOGIN_ENDPOINT"] = os.getenv("LOGIN_ENDPOINT", "/login").strip()
    config["SITE_CREATE_PAGE_ENDPOINT"] = os.getenv("SITE_CREATE_PAGE_ENDPOINT", "/site/create").strip()
    config["SITE_ENDPOINT"] = os.getenv("SITE_ENDPOINT", "/site").strip()

    config["ADMIN_BASE_URL"] = config["ADMIN_BASE_URL"].rstrip("/")

    config["LOGIN_PATH"] = os.getenv("LOGIN_PATH", "/login").strip()
    config["DASHBOARD_PATH"] = os.getenv("DASHBOARD_PATH", "/dashboard").strip()
    config["SITE_CREATE_PATH"] = os.getenv("SITE_CREATE_PATH", "/site/create").strip()
    config["SITES_LIST_PATH"] = os.getenv("SITES_LIST_PATH", "/site").strip()

    return config

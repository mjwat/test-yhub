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
        "TEST_USER_EMAIL": _get_required_value("TEST_USER_EMAIL", "AUTH_USER_EMAIL"),
        "TEST_USER_PASSWORD": _get_required_value("TEST_USER_PASSWORD", "AUTH_USER_PASSWORD"),
    }

    config["CSRF_ENDPOINT"] = os.getenv("CSRF_ENDPOINT", "/sanctum/csrf-cookie").strip()
    config["LOGIN_ENDPOINT"] = os.getenv("LOGIN_ENDPOINT", "/login").strip()
    config["AUTH_CHECK_ENDPOINT"] = os.getenv(
        "AUTH_CHECK_ENDPOINT",
        os.getenv("TOKEN_VALIDATION_ENDPOINT", "/api/user"),
    ).strip()

    return config

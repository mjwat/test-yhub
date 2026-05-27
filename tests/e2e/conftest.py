import os
from typing import Dict

import pytest


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

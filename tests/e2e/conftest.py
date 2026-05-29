import os
from typing import Dict

import allure
import pytest
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page


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


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when not in {"setup", "call"} or not report.failed:
        return

    page = item.funcargs.get("page")
    if not isinstance(page, Page) or page.is_closed():
        return

    try:
        screenshot = page.screenshot()
    except PlaywrightError:
        return

    attachment_name = f"failure-screenshot::{item.name}::{report.when}"
    allure.attach(
        screenshot,
        name=attachment_name,
        attachment_type=allure.attachment_type.PNG,
    )

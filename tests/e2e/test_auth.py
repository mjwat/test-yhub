import re
from typing import Dict

import allure
from playwright.sync_api import Page, expect

from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.login_page import LoginPage


## YH-UI-AU-001: Successful login with valid credentials

@allure.feature("Authentication")
@allure.title("User can log in with valid credentials")
def test_successful_login (
    page: Page,
    user_credentials: Dict[str, str],
    login_path: str,
    dashboard_path: str,
) -> None:
    login_page = LoginPage(page)
    login_page.navigate(login_path)
    login_page.login_action(user_credentials["email"], user_credentials["password"])

    dashboard_page = DashboardPage(page)
    expect(page).to_have_url(re.compile(dashboard_path))

    is_dashboard_link_visible = dashboard_page.navigation.dashboard_link.first.is_visible()

    assert is_dashboard_link_visible, (
        "Expected logged-in UI indicator to be visible after login. "
        "Dashboard link is not visible."
    )

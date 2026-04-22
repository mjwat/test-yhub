import re
from typing import Dict

from playwright.sync_api import Page, expect

from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.login_page import LoginPage


## YH-UI-AU-001: Successful login with valid credentials

def test_successful_login (
    page: Page,
    ui_user: Dict[str, str],
    login_path: str,
    dashboard_path: str,
) -> None:
    login_page = LoginPage(page)
    login_page.navigate(login_path)
    login_page.login_action(ui_user["email"], ui_user["password"])

    dashboard_page = DashboardPage(page)
    expect(page).to_have_url(re.compile(dashboard_path))

    is_logout_visible = dashboard_page.sidebar.logout_link.first.is_visible()

    assert is_logout_visible, (
        "Expected logged-in UI indicator to be visible after login. "
        "Logout link is not visible."
    )

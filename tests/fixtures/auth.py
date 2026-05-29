import re
from typing import Dict

import allure
import pytest
from playwright.sync_api import Page, expect

from clients.auth_client import AuthClient
from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.login_page import LoginPage
from utils.url import url_contains_expected


@pytest.fixture(scope="function")
def api_base_url(base_url: str) -> str:
    return base_url


@pytest.fixture(scope="session")
def user_credentials(env_config: Dict[str, str]) -> Dict[str, str]:
    return {
        "email": env_config["TEST_USER_EMAIL"],
        "password": env_config["TEST_USER_PASSWORD"],
    }


@pytest.fixture(scope="function")
def auth_client(api_base_url: str, env_config: Dict[str, str]) -> AuthClient:
    return AuthClient(
        base_url=api_base_url,
        csrf_endpoint=env_config["CSRF_ENDPOINT"],
        login_endpoint=env_config["LOGIN_ENDPOINT"],
    )


@pytest.fixture(scope="function")
def logged_in_client(auth_client: AuthClient, user_credentials: Dict[str, str]) -> AuthClient:
    with allure.step("Prepare an authenticated API client"):
        auth_response = auth_client.authenticate(
            email=user_credentials["email"],
            password=user_credentials["password"],
        )
        if auth_response.status_code not in (200, 204):
            raise RuntimeError(
                f"Authentication failed. Status code: {auth_response.status_code}. "
                f"URL: {auth_response.request.url}. Body: {auth_response.text[:500]}"
            )
    return auth_client


@pytest.fixture(scope="function")
def logged_in_admin(
    page: Page,
    user_credentials: Dict[str, str],
    login_path: str,
    admin_base_url: str,
) -> DashboardPage:
    login_page = LoginPage(page)
    with allure.step("Log in to the admin UI as a valid user"):
        login_page.navigate(login_path)
        login_page.login_action(user_credentials["email"], user_credentials["password"])

    with allure.step("Verify the admin area is opened after login"):
        expect(page).to_have_url(re.compile(rf".*{re.escape(admin_base_url)}.*"), timeout=5_000)

        assert url_contains_expected(page.url, admin_base_url), (
            "Expected final UI URL to point to admin area after login. "
            f"Admin URL: {admin_base_url}. Final URL: {page.url}"
        )
    return DashboardPage(page)

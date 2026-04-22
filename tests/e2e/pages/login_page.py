import re

from playwright.sync_api import Locator, Page

from tests.e2e.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_field: Locator = page.get_by_label(re.compile("email", re.IGNORECASE))
        self.password_field: Locator = page.get_by_label(re.compile("password", re.IGNORECASE))
        self.login_button: Locator = page.get_by_role("button", name=re.compile("log ?in", re.IGNORECASE))

    def login_action(self, email: str, password: str) -> None:
        self.email_field.fill(email)
        self.password_field.fill(password)
        self.login_button.click()

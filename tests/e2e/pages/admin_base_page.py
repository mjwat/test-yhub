from playwright.sync_api import Page

from tests.e2e.components.navigation import Navigation
from tests.e2e.pages.base_page import BasePage


class AdminBasePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.navigation = Navigation(page)

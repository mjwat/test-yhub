from playwright.sync_api import Page

from tests.e2e.pages.admin_base_page import AdminBasePage


class DashboardPage(AdminBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

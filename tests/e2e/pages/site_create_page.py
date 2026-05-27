import re

from playwright.sync_api import Locator, Page, expect

from tests.e2e.pages.admin_base_page import AdminBasePage


class SiteCreatePage(AdminBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.git_repo_input: Locator = page.get_by_placeholder(re.compile("github", re.IGNORECASE)).first
        self.create_button: Locator = page.get_by_role("button", name=re.compile("create", re.IGNORECASE)).first

    def create_from_git(self, repo_url: str) -> None:
        expect(self.git_repo_input).to_be_visible(timeout=20_000)
        self.git_repo_input.fill(repo_url)
        
        expect(self.create_button).to_be_enabled()
        self.create_button.click()

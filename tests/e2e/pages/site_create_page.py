import re

from playwright.sync_api import Locator, Page, expect

from tests.e2e.pages.admin_base_page import AdminBasePage


class SiteCreatePage(AdminBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.github_repository_button: Locator = page.get_by_role("button", 
            name=re.compile(r"github", re.IGNORECASE)).first
        self.git_repo_input: Locator = page.get_by_placeholder(re.compile("github", re.IGNORECASE)).first
        self.create_button: Locator = page.get_by_role("button", name=re.compile("Создать проект", re.IGNORECASE)).first

    def choose_github_repository(self) -> None:
        expect(self.github_repository_button).to_be_visible(timeout=20_000)
        self.github_repository_button.click()

    def create_from_git(self, repo_url: str) -> None:
        self.choose_github_repository()
        expect(self.git_repo_input).to_be_visible(timeout=20_000)
        self.git_repo_input.fill(repo_url)

        expect(self.create_button).to_be_enabled()
        self.create_button.click()

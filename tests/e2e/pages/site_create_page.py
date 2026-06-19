import re
from typing import Literal, Optional

from playwright.sync_api import Locator, Page, expect

from tests.e2e.pages.admin_base_page import AdminBasePage


class SiteCreatePage(AdminBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.github_repository_button: Locator = page.get_by_role("button",
            name=re.compile(r"github", re.IGNORECASE)).first
        self.editor_button: Locator = page.get_by_role(
            "button",
            name=re.compile(r"editor", re.IGNORECASE),
        ).first
        self.git_repo_input: Locator = page.get_by_placeholder(re.compile("github", re.IGNORECASE)).first
        self.custom_domain_input: Locator = page.get_by_placeholder("my-awesome-project").first
        self.single_file_input: Locator = page.locator("input[type='file']:not([webkitdirectory])").first
        self.folder_input: Locator = page.locator("input[type='file'][webkitdirectory]").first
        self.create_button: Locator = page.get_by_role("button", name=re.compile("Создать проект", re.IGNORECASE)).first

    def _fill_custom_domain(self, custom_domain: str) -> None:
        expect(self.custom_domain_input).to_be_visible(timeout=20_000)
        self.custom_domain_input.fill(custom_domain)

    def _upload_single_file(self, upload_path: str) -> None:
        expect(self.single_file_input).to_be_attached(timeout=20_000)
        self.single_file_input.set_input_files(upload_path)

    def _upload_folder(self, folder_path: str) -> None:
        expect(self.folder_input).to_be_attached(timeout=20_000)
        self.folder_input.set_input_files(folder_path)

    def _submit_project_creation(self) -> None:
        expect(self.create_button).to_be_enabled()
        self.create_button.click()

    def _require_value(self, value: Optional[str], field_name: str, source: str) -> str:
        if value is None:
            raise ValueError(f"`{field_name}` is required for site creation via `{source}`.")
        return value

    def choose_github_tab(self) -> None:
        expect(self.github_repository_button).to_be_visible(timeout=20_000)
        self.github_repository_button.click()

    def choose_editor_tab(self) -> None:
        expect(self.editor_button).to_be_visible(timeout=20_000)
        self.editor_button.click()

    def create_site(
        self,
        source: Literal["git", "upload_file", "upload_folder", "editor"],
        repo_url: Optional[str] = None,
        upload_path: Optional[str] = None,
        custom_domain: Optional[str] = None,
    ) -> None:
        if source == "git":
            self.choose_github_tab()
            expect(self.git_repo_input).to_be_visible(timeout=20_000)
            self.git_repo_input.fill(self._require_value(repo_url, "repo_url", source))
        elif source == "upload_file":
            self._upload_single_file(self._require_value(upload_path, "upload_path", source))
        elif source == "upload_folder":
            self._upload_folder(self._require_value(upload_path, "upload_path", source))
        elif source == "editor":
            self.choose_editor_tab()

        if custom_domain is not None:
            self._fill_custom_domain(custom_domain)

        self._submit_project_creation()

    def create_via_git(self, repo_url: str, custom_domain: Optional[str] = None) -> None:
        self.create_site(source="git", repo_url=repo_url, custom_domain=custom_domain)

    def create_via_upload_file(self, upload_path: str, custom_domain: Optional[str] = None) -> None:
        self.create_site(source="upload_file", upload_path=upload_path, custom_domain=custom_domain)

    def create_via_upload_folder(self, folder_path: str, custom_domain: Optional[str] = None) -> None:
        self.create_site(source="upload_folder", upload_path=folder_path, custom_domain=custom_domain)

    def create_via_editor(self, custom_domain: Optional[str] = None) -> None:
        self.create_site(source="editor", custom_domain=custom_domain)

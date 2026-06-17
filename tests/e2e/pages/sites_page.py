import re

from playwright.sync_api import Locator, Page, expect

from tests.e2e.pages.admin_base_page import AdminBasePage


class SitesPage(AdminBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.site_rows: Locator = page.locator("//main/div/article")

    def assert_sites_list_page_opened(self, sites_list_path: str) -> None:
        expect(self.page).to_have_url(re.compile(rf".*{re.escape(sites_list_path)}(/)?([?#].*)?$"))

    def first_site_row(self) -> Locator:
        row = self.site_rows.first
        expect(row).to_be_visible(timeout=60_000)
        return row

    def assert_first_site_status_created(self) -> None:
        expect(self.first_site_row()).to_contain_text(re.compile("Идет публикация", re.IGNORECASE), timeout=120_000)
        # expect(self.first_site_row()).to_contain_text(re.compile("created", re.IGNORECASE), timeout=120_000)

    def assert_first_site_contains_domain(self, expected_domain: str) -> None:
        expect(self.first_site_row()).to_contain_text(
            re.compile(re.escape(expected_domain), re.IGNORECASE),
            timeout=60_000,
        )

    def wait_for_first_site_status_active(self) -> None:
        expect(self.first_site_row()).to_contain_text(re.compile("Опубликован", re.IGNORECASE), timeout=60_000)
            # expect(self.first_site_row()).to_contain_text(re.compile("active", re.IGNORECASE), timeout=60_000)


    def generated_site_link(self) -> Locator:
        link = self.first_site_row().locator("a[href^='http']").first
        expect(link).to_be_visible(timeout=60_000)
        return link

    def site_button(self) -> Locator:
        button = self.first_site_row().get_by_label(re.compile("Открыть сайт", re.IGNORECASE)).first
        expect(button).to_be_visible(timeout=60_000)
        return button

    def open_generated_site_in_new_tab(self) -> Page:
        site_link = self.site_button()
        with self.page.expect_popup(timeout=60_000) as popup_context:
            site_link.click()
        popup = popup_context.value
        popup.wait_for_load_state("domcontentloaded", timeout=60_000)
        return popup

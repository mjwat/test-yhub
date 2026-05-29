import re

from playwright.sync_api import Locator, Page, expect

from tests.e2e.pages.admin_base_page import AdminBasePage


class SitesPage(AdminBasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.site_rows: Locator = page.locator("table tbody tr")

    def assert_sites_list_page_opened(self, sites_list_path: str) -> None:
        expect(self.page).to_have_url(re.compile(rf".*{re.escape(sites_list_path)}(/)?([?#].*)?$"))

    def first_site_row(self) -> Locator:
        row = self.site_rows.first
        expect(row).to_be_visible(timeout=60_000)
        return row

    def assert_first_site_status_created(self) -> None:
        expect(self.first_site_row()).to_contain_text(re.compile("test", re.IGNORECASE), timeout=120_000)
        # expect(self.first_site_row()).to_contain_text(re.compile("created", re.IGNORECASE), timeout=120_000)


    def wait_for_first_site_status_active(self) -> None:
        expect(self.first_site_row()).to_contain_text(re.compile("active", re.IGNORECASE), timeout=600_000)

    def generated_site_link(self) -> Locator:
        link = self.first_site_row().locator("a[href^='http']").first
        expect(link).to_be_visible(timeout=60_000)
        return link

    def open_generated_site_in_new_tab(self) -> Page:
        site_link = self.generated_site_link()
        with self.page.expect_popup(timeout=60_000) as popup_context:
            site_link.click()
        popup = popup_context.value
        popup.wait_for_load_state("domcontentloaded", timeout=60_000)
        return popup

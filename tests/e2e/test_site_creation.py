import logging
import re

import allure
from playwright.sync_api import expect

from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.site_create_page import SiteCreatePage
from tests.e2e.pages.sites_page import SitesPage

logger = logging.getLogger(__name__)


## YH-UI-SC-001: Create site from Git repository URL

@allure.feature("Site Creation")
@allure.title("User can create a site from a Git repository URL")
def test_create_site_from_git(
    logged_in_admin: DashboardPage,
    clean_user_sites: None,
    git_repo_url: str,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from the Git repository URL"):
        site_create_page.create_from_git(git_repo_url)

    sites_page = SitesPage(logged_in_admin.page)
    with allure.step("Verify the new site appears in the sites list"):
        sites_page.assert_sites_list_page_opened(sites_list_path)

        sites_page.assert_first_site_status_created()

    with allure.step("Verify the generated site becomes active and accessible"):
        sites_page.wait_for_first_site_status_active()
 
        generated_link = sites_page.generated_site_link()
        generated_href = generated_link.get_attribute("href")
        assert generated_href and generated_href.strip(), "Expected generated site link to have non-empty href."

        popup = sites_page.open_generated_site_in_new_tab()
        expect(popup).to_have_url(re.compile(r"^https?://"))
        expect(popup.locator("body")).to_be_visible()
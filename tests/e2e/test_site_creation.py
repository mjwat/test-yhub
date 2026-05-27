import logging
import re

from playwright.sync_api import expect

from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.site_create_page import SiteCreatePage
from tests.e2e.pages.sites_page import SitesPage

logger = logging.getLogger(__name__)


## YH-UI-SC-001: Create site from Git repository URL

def test_create_site_from_git(
    logged_in_admin: DashboardPage,
    clean_user_sites: None,
    git_repo_url: str,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    logger.info("Opening site creation page: %s", site_create_path)
    site_create_page = SiteCreatePage(logged_in_admin.page)
    site_create_page.navigate(site_create_path)

    logger.info("Creating site from Git repository URL: %s", git_repo_url)
    site_create_page.create_from_git(git_repo_url)

    sites_page = SitesPage(logged_in_admin.page)
    logger.info("Verifying redirect to sites list page: %s", sites_list_path)
    sites_page.assert_sites_list_page_opened(sites_list_path)

    logger.info("Checking initial site status is Created")
    sites_page.assert_first_site_status_created()

    logger.info("Waiting for site status to become Active")
    sites_page.wait_for_first_site_status_active()

    generated_link = sites_page.generated_site_link()
    generated_href = generated_link.get_attribute("href")
    assert generated_href and generated_href.strip(), "Expected generated site link to have non-empty href."

    logger.info("Opening generated site link in a new tab: %s", generated_href)
    popup = sites_page.open_generated_site_in_new_tab()
    expect(popup).to_have_url(re.compile(r"^https?://"))
    expect(popup.locator("body")).to_be_visible()
    logger.info("Generated site opened successfully")

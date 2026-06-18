import logging
from pathlib import Path
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

    with allure.step("Verify the generated site becomes active"):
        sites_page.wait_for_first_site_status_active()
 
    with allure.step("Verify the generated site is accessible"):
        popup = sites_page.open_generated_site_in_new_tab()
        expect(popup).to_have_url(re.compile(r"^https?://"))
        expect(popup.locator("body")).to_be_visible()



## YH-UI-SC-002: Create site from single file and with custom domain

@allure.feature("Site Creation")
@allure.title("User can create a site from a single file with custom domain")
def test_create_site_from_single_file_with_custom_domain(
    logged_in_admin: DashboardPage,
    clean_user_sites: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    custom_domain = "my-test-domain"
    html_file_path = Path(__file__).resolve().parents[2] / "data" / "index.html"

    assert html_file_path.is_file(), (
        "Expected HTML upload file to exist for the single-file site creation test. "
        f"Missing file: {html_file_path}"
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from a single HTML file with custom domain"):
        site_create_page.create_from_upload(str(html_file_path), custom_domain=custom_domain)

    sites_page = SitesPage(logged_in_admin.page)
    with allure.step("Verify the new site appears in the sites list"):
        sites_page.assert_sites_list_page_opened(sites_list_path)
        sites_page.assert_first_site_status_created()

    with allure.step("Verify the generated site becomes active and keeps the custom domain"):
        sites_page.wait_for_first_site_status_active()
        sites_page.assert_first_site_contains_domain(custom_domain)

    with allure.step("Verify the generated site is accessible"):
        popup = sites_page.open_generated_site_in_new_tab()
        expect(popup).to_have_url(re.compile(r"^https?://"))
        expect(popup.locator("body")).to_be_visible()


## YH-UI-SC-003: Create site from archive

@allure.feature("Site Creation")
@allure.title("User can create a site from an archive")
def test_create_site_from_archive(
    logged_in_admin: DashboardPage,
    clean_user_sites: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    archive_file_path = Path(__file__).resolve().parents[2] / "data" / "archive.zip"

    assert archive_file_path.is_file(), (
        "Expected archive upload file to exist for the archive site creation test. "
        f"Missing file: {archive_file_path}"
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from an archive file"):
        site_create_page.create_from_upload(str(archive_file_path))

    sites_page = SitesPage(logged_in_admin.page)
    with allure.step("Verify the new site appears in the sites list"):
        sites_page.assert_sites_list_page_opened(sites_list_path)
        sites_page.assert_first_site_status_created()

    with allure.step("Verify the generated site becomes active"):
        sites_page.wait_for_first_site_status_active()

    with allure.step("Verify the generated site is accessible"):
        popup = sites_page.open_generated_site_in_new_tab()
        expect(popup).to_have_url(re.compile(r"^https?://"))
        expect(popup.locator("body")).to_be_visible()


## YH-UI-SC-004: Create site with pdf

@allure.feature("Site Creation")
@allure.title("User can create a site from a PDF file")
def test_create_site_from_pdf(
    logged_in_admin: DashboardPage,
    clean_user_sites: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    pdf_file_path = Path(__file__).resolve().parents[2] / "data" / "sample.pdf"

    assert pdf_file_path.is_file(), (
        "Expected PDF upload file to exist for the PDF site creation test. "
        f"Missing file: {pdf_file_path}"
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from a PDF file"):
        site_create_page.create_from_upload(str(pdf_file_path))

    sites_page = SitesPage(logged_in_admin.page)
    with allure.step("Verify the new site appears in the sites list"):
        sites_page.assert_sites_list_page_opened(sites_list_path)
        sites_page.assert_first_site_status_created()

    with allure.step("Verify the generated site becomes active"):
        sites_page.wait_for_first_site_status_active()

    with allure.step("Verify the generated site is available"):
        popup = sites_page.open_generated_site_in_new_tab()
        expect(popup).to_have_url(re.compile(r"^https?://"))
        popup.wait_for_load_state("domcontentloaded", timeout=60_000)
        assert not popup.is_closed(), "Expected generated PDF site tab to remain open after loading."


## YH-UI-SC-005: Create site from folder via drag and drop

@allure.feature("Site Creation")
@allure.title("User can create a site from a folder via drag and drop")
def test_create_site_from_folder_drag_and_drop(
    logged_in_admin: DashboardPage,
    clean_user_sites: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    folder_path = Path(__file__).resolve().parents[2] / "data" / "simple_html_css"

    assert folder_path.is_dir(), (
        "Expected folder upload test directory to exist for the folder drag-and-drop site creation test. "
        f"Missing directory: {folder_path}"
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from a folder via drag and drop upload"):
        site_create_page.create_from_folder(str(folder_path))

    sites_page = SitesPage(logged_in_admin.page)
    with allure.step("Verify the new site appears in the sites list"):
        sites_page.assert_sites_list_page_opened(sites_list_path)
        sites_page.assert_first_site_status_created()

    with allure.step("Verify the generated site becomes active"):
        sites_page.wait_for_first_site_status_active()

    with allure.step("Verify the generated site is accessible"):
        popup = sites_page.open_generated_site_in_new_tab()
        expect(popup).to_have_url(re.compile(r"^https?://"))
        expect(popup.locator("body")).to_be_visible()

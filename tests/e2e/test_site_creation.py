import logging
from pathlib import Path
import re
from typing import Callable, Optional

import allure
from playwright.sync_api import Page, expect

from tests.e2e.pages.dashboard_page import DashboardPage
from tests.e2e.pages.site_create_page import SiteCreatePage
from tests.e2e.pages.sites_page import SitesPage

logger = logging.getLogger(__name__)

TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


## YH-UI-SC-001: Create site from Git repository URL

@allure.feature("Site Creation")
@allure.title("User can create a site from a Git repository URL")
def test_create_site_from_git(
    logged_in_admin: DashboardPage,
    ensure_site_creation_available: None,
    git_repo_url: str,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from the Git repository URL"):
        site_create_page.create_via_git(git_repo_url)

    _verify_created_site(logged_in_admin.page, sites_list_path)



## YH-UI-SC-002: Create site from single file and with custom domain

@allure.feature("Site Creation")
@allure.title("User can create a site from a single file with custom domain")
def test_create_site_from_single_file_with_custom_domain(
    logged_in_admin: DashboardPage,
    ensure_site_creation_available: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    custom_domain = "my-test-domain"
    html_file_path = _get_required_test_file(
        "index.html",
        "Expected HTML upload file to exist for the single-file site creation test. "
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from a single HTML file with custom domain"):
        site_create_page.create_via_upload_file(str(html_file_path), custom_domain=custom_domain)

    _verify_created_site(
        logged_in_admin.page,
        sites_list_path,
        expected_domain=custom_domain,
    )


## YH-UI-SC-003: Create site from archive

@allure.feature("Site Creation")
@allure.title("User can create a site from an archive")
def test_create_site_from_archive(
    logged_in_admin: DashboardPage,
    ensure_site_creation_available: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    archive_file_path = _get_required_test_file(
        "archive.zip",
        "Expected archive upload file to exist for the archive site creation test. "
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from an archive file"):
        site_create_page.create_via_upload_file(str(archive_file_path))

    _verify_created_site(logged_in_admin.page, sites_list_path)


## YH-UI-SC-004: Create site with pdf

@allure.feature("Site Creation")
@allure.title("User can create a site from a PDF file")
def test_create_site_from_pdf(
    logged_in_admin: DashboardPage,
    ensure_site_creation_available: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    pdf_file_path = _get_required_test_file(
        "sample.pdf",
        "Expected PDF upload file to exist for the PDF site creation test. "
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from a PDF file"):
        site_create_page.create_via_upload_file(str(pdf_file_path))

    _verify_created_site(
        logged_in_admin.page,
        sites_list_path,
        accessibility_assertion=_assert_generated_pdf_site_available,
    )


## YH-UI-SC-005: Create site from folder via drag and drop

@allure.feature("Site Creation")
@allure.title("User can create a site from a folder via drag and drop")
def test_create_site_from_folder_drag_and_drop(
    logged_in_admin: DashboardPage,
    ensure_site_creation_available: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    folder_path = _get_required_test_directory(
        "simple_html_css",
        "Expected folder upload test directory to exist for the folder drag-and-drop site creation test. "
    )

    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from a folder via drag and drop upload"):
        site_create_page.create_via_upload_folder(str(folder_path))

    _verify_created_site(logged_in_admin.page, sites_list_path)


## YH-UI-SC-007: Create site by code editor

@allure.feature("Site Creation")
@allure.title("User can create a site from the default code editor project")
def test_create_site_from_code_editor(
    logged_in_admin: DashboardPage,
    ensure_site_creation_available: None,
    site_create_path: str,
    sites_list_path: str,
) -> None:
    site_create_page = SiteCreatePage(logged_in_admin.page)
    with allure.step("Open the site creation page"):
        site_create_page.navigate(site_create_path)

    with allure.step("Create a site from the default code editor project"):
        site_create_page.create_via_editor()

    _verify_created_site(logged_in_admin.page, sites_list_path)



def _get_required_test_file(file_name: str, assertion_message: str) -> Path:
    file_path = TEST_DATA_DIR / file_name
    assert file_path.is_file(), f"{assertion_message} Missing file: {file_path}"
    return file_path


def _get_required_test_directory(directory_name: str, assertion_message: str) -> Path:
    directory_path = TEST_DATA_DIR / directory_name
    assert directory_path.is_dir(), f"{assertion_message} Missing directory: {directory_path}"
    return directory_path


def _assert_generated_site_available(popup: Page) -> None:
    expect(popup).to_have_url(re.compile(r"^https?://"))
    expect(popup.locator("body")).to_be_visible()


def _assert_generated_pdf_site_available(popup: Page) -> None:
    expect(popup).to_have_url(re.compile(r"^https?://"))
    popup.wait_for_load_state("domcontentloaded", timeout=60_000)
    assert not popup.is_closed(), "Expected generated PDF site tab to remain open after loading."


def _verify_created_site(
    page: Page,
    sites_list_path: str,
    expected_domain: Optional[str] = None,
    accessibility_assertion: Callable[[Page], None] = _assert_generated_site_available,
) -> None:
    sites_page = SitesPage(page)

    with allure.step("Verify the new site appears in the sites list"):
        sites_page.assert_sites_list_page_opened(sites_list_path)
        sites_page.assert_first_site_status_created()

    with allure.step("Verify the generated site becomes active"):
        sites_page.wait_for_first_site_status_active()

    if expected_domain is not None:
        with allure.step("Verify the generated site keeps the custom domain"):
            sites_page.assert_first_site_contains_domain(expected_domain)

    with allure.step("Verify the generated site is accessible"):
        popup = sites_page.open_generated_site_in_new_tab()
        accessibility_assertion(popup)

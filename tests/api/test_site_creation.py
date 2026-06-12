import allure

from clients.site_client import SiteClient
from utils.url import build_url
from utils.url import url_contains_expected


## YH-API-SC-001: Site Creation Page is available for authenticated user

@allure.feature("Site Creation")
@allure.title("Authenticated user can open the site creation page")
def test_site_creation_page_available_for_authenticated_user(
    admin_base_url: str,
    dashboard_deploy_path: str,
    site_client: SiteClient,
    clean_user_sites: None,
) -> None:
    response = site_client.get_site_creation_page()
    expected_url = build_url(admin_base_url, dashboard_deploy_path)

    assert response.status_code == 200, (
        f"Expected status code 200 for site creation page, got {response.status_code}. "
        f"Final URL: {response.url}. Body: {response.text[:500]}"
    )

    assert response.url == expected_url, (
        "Expected final URL to point to the dashboard deploy view. "
        f"Expected URL: {expected_url}. Final URL: {response.url}"
    )


# YH-API-SC-002: Create site from Git repository URL

@allure.feature("Site Creation")
@allure.title("User can create a site from a Git repository URL")
def test_site_creation_by_git(
    site_client: SiteClient,
    git_repo_url: str,
    clean_user_sites: None,
) -> None:
    with allure.step("Create a site from the Git repository URL"):
        create_result = site_client.create_site_from_git_url(git_repo_url)

    with allure.step("Verify the create-site request completes successfully"):
        assert create_result["initial_status_code"] == 302, (
            f"Expected create-by-git response status 302, got {create_result['initial_status_code']}. "
            f"Create result: {create_result}"
        )

        location_header = create_result["redirect_location"]
        assert location_header, "Expected redirect Location header in create-by-git response."

        assert url_contains_expected(location_header, site_client.site_endpoint), (
            "Expected redirect location to point to sites list page. "
            f"Expected endpoint: {site_client.site_endpoint}, Location: {location_header}"
        )

        assert create_result["flash_message"] == "Site created successfully, and files uploaded.", (
            "Expected success flash message after create-by-git redirect. "
            f"Got: {create_result['flash_message']}"
        )

    with allure.step("Verify the new site appears in the sites list"):
        sites_after_creation = site_client.get_user_sites()
        assert len(sites_after_creation) == 1, (
            f"Expected exactly 1 site after creation, got {len(sites_after_creation)}. "
            f"Sites: {sites_after_creation}"
        )

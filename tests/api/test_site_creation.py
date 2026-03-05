from clients.site_client import SiteClient


## YH-SC-001: Site Creation Page is available for authenticated user

def test_site_creation_page_available_for_authenticated_user(site_client: SiteClient) -> None:
    response = site_client.get_site_creation_page()

    assert response.status_code == 200, (
        f"Expected status code 200 for site creation page, got {response.status_code}. "
        f"Final URL: {response.url}. Body: {response.text[:500]}"
    )

    expected_endpoint = site_client.site_create_page_endpoint.lower().rstrip("/")
    final_url = response.url.lower().rstrip("/")
    assert expected_endpoint in final_url, (
        "Expected final URL to point to the site creation page, "
        f"expected endpoint: {site_client.site_create_page_endpoint}, final URL: {response.url}"
    )


# YH-SC-002: Create site from Git repository URL

def test_site_creation_by_git(
    site_client: SiteClient,
    git_repo_url: str,
    # ensure_no_sites: None,
) -> None:
    response = site_client.create_site_from_git_url(git_repo_url)

    assert response.status_code == 302, (
        f"Expected create-by-git response status 302, got {response.status_code}. "
        f"URL: {response.url}. Body: {response.text[:500]}"
    )

    location_header = response.headers.get("Location")
    assert location_header, "Expected redirect Location header in create-by-git response."

    expected_list_endpoint = site_client.site_endpoint.lower().rstrip("/")
    actual_location = location_header.lower().rstrip("/")
    assert expected_list_endpoint in actual_location, (
        "Expected redirect location to point to sites list page. "
        f"Expected endpoint: {site_client.site_endpoint}, Location: {location_header}"
    )

    sites_after_creation = site_client.get_user_sites()
    assert len(sites_after_creation) == 1, (
        f"Expected exactly 1 site after creation, got {len(sites_after_creation)}. "
        f"Sites: {sites_after_creation}"
    )

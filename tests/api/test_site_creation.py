from clients.site_client import SiteClient


def test_site_creation_page_available_for_authenticated_user(site_client: SiteClient) -> None:
    response = site_client.get_site_creation_page()

    assert response.status_code == 200, (
        f"Expected status code 200 for site creation page, got {response.status_code}. "
        f"Final URL: {response.url}. Body: {response.text[:500]}"
    )

    expected_endpoint = site_client.site_create_endpoint.lower().rstrip("/")
    final_url = response.url.lower().rstrip("/")
    assert expected_endpoint in final_url, (
        "Expected final URL to point to the site creation page, "
        f"expected endpoint: {site_client.site_create_endpoint}, final URL: {response.url}"
    )

from typing import Dict

from clients.auth_client import AuthClient
from utils.url import url_contains_expected


## YH-API-AU-001: Successful login with valid credentials

def test_successful_login_with_valid_credentials(
    auth_client: AuthClient,
    user_credentials: Dict[str, str],
    admin_base_url: str,
) -> None:
    token = auth_client.get_csrf_token()

    response = auth_client.login(
        email=user_credentials["email"],
        password=user_credentials["password"],
        token=token,
    )

    assert response.status_code == 200, (
        f"Expected login status 200, got {response.status_code}. "
        f"URL: {response.request.url}. Body: {response.text}"
    )

    assert url_contains_expected(response.url, admin_base_url), (
        "Expected final response URL to point to admin area after login. "
        f"Admin URL: {admin_base_url}. Final URL: {response.url}"
    )

from typing import Dict

from clients.auth_client import AuthClient


def test_successful_login_with_valid_credentials(
    auth_client: AuthClient,
    test_user: Dict[str, str],
) -> None:
    token = auth_client.get_csrf_token()

    response = auth_client.login(
        email=test_user["email"],
        password=test_user["password"],
        token=token,
    )

    assert response.status_code == 200, (
        f"Expected login status 200, got {response.status_code}. "
        f"URL: {response.request.url}. Body: {response.text}"
    )

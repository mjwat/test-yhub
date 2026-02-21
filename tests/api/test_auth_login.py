from typing import Dict

from clients.auth_client import AuthClient


def test_successful_login_with_valid_credentials(
    auth_client: AuthClient,
    valid_login_payload: Dict[str, str],
) -> None:
    csrf_response = auth_client.get_csrf_cookie()

    assert csrf_response.status_code in (200, 204), (
        f"Expected CSRF init status 200/204, got {csrf_response.status_code}. "
        f"URL: {csrf_response.request.url}. Body: {csrf_response.text}"
    )

    xsrf_token = auth_client.get_xsrf_token()
    assert xsrf_token is not None, "Expected XSRF-TOKEN cookie after CSRF initialization."
    assert xsrf_token.strip(), "Expected XSRF-TOKEN cookie value to be non-empty."

    cookie_names = set(auth_client.session.cookies.keys())
    assert "laravel_session" in cookie_names, "Expected 'laravel_session' cookie after CSRF initialization."

    login_response = auth_client.login(
        email=valid_login_payload["email"],
        password=valid_login_payload["password"],
        xsrf_token=xsrf_token,
    )

    assert login_response.status_code in (200, 204), (
        f"Expected login status 200/204, got {login_response.status_code}. "
        f"URL: {login_response.request.url}. Body: {login_response.text}"
    )

    validation_response = auth_client.get_current_user()

    assert validation_response.status_code == 200, (
        f"Expected authenticated session check status 200, got {validation_response.status_code}. "
        f"URL: {validation_response.request.url}. Body: {validation_response.text}"
    )

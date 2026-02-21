from clients.auth_client import AuthClient


def test_successful_login_with_valid_credentials(
    authenticated_session: AuthClient,
) -> None:
    cookie_names = set(authenticated_session.session.cookies.keys())
    session_cookies = {name for name in cookie_names if name.endswith("_session")}
    assert session_cookies, (
        "Expected a session cookie (e.g. 'laravel_session' or '<app>_session') "
        f"after CSRF/login flow, got: {sorted(cookie_names)}"
    )

import logging
from typing import Optional
from urllib.parse import unquote

import requests

logger = logging.getLogger(__name__)


class AuthClient:
    def __init__(
        self,
        base_url: str,
        login_endpoint: str = "/login",
        csrf_endpoint: str = "/sanctum/csrf-cookie",
        auth_check_endpoint: str = "/api/user",
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.login_endpoint = login_endpoint
        self.csrf_endpoint = csrf_endpoint
        self.auth_check_endpoint = auth_check_endpoint
        self.session = session or requests.Session()

    def _build_url(self, path: str) -> str:
        normalized_path = path if path.startswith("/") else f"/{path}"
        return f"{self.base_url}{normalized_path}"

    def get_csrf_cookie(self) -> requests.Response:
        csrf_url = self._build_url(self.csrf_endpoint)
        logger.info("CSRF request: GET %s", csrf_url)
        response = self.session.get(url=csrf_url)
        logger.info("CSRF response: status=%s url=%s", response.status_code, csrf_url)
        return response

    def get_xsrf_token(self) -> Optional[str]:
        token = self.session.cookies.get("XSRF-TOKEN")
        if token is None:
            return None
        return unquote(token)

    def login(self, email: str, password: str, xsrf_token: str) -> requests.Response:
        login_url = self._build_url(self.login_endpoint)
        payload = {"email": email, "password": password}
        masked_payload = {"email": email, "password": "***"}
        headers = {
            "X-XSRF-TOKEN": xsrf_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        logger.info("Login request: POST %s payload=%s", login_url, masked_payload)
        response = self.session.post(
            url=login_url,
            json=payload,
            headers=headers,
        )
        logger.info("Login response: status=%s url=%s", response.status_code, login_url)
        return response

    def get_current_user(self) -> requests.Response:
        user_url = self._build_url(self.auth_check_endpoint)
        logger.info("Session auth check request: GET %s", user_url)
        response = self.session.get(
            url=user_url,
            headers={"Accept": "application/json"},
        )
        logger.info("Session auth check response: status=%s url=%s", response.status_code, user_url)
        return response

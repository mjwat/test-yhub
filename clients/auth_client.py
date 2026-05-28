from typing import Optional

import allure
import requests

from clients.base_api_client import BaseApiClient


class AuthClient(BaseApiClient):
    def __init__(
        self,
        base_url: str,
        login_endpoint: str,
        csrf_endpoint: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        super().__init__(base_url=base_url, session=session)
        self.login_endpoint = login_endpoint
        self.csrf_endpoint = csrf_endpoint

    def get_csrf_cookie(self) -> requests.Response:
        csrf_url = self.build_url(self.csrf_endpoint)
        self.logger.info("CSRF request: GET %s", csrf_url)
        response = self.get(self.csrf_endpoint)
        self.logger.info("CSRF response: status=%s url=%s", response.status_code, csrf_url)
        return response

    def get_csrf_token(self) -> str:
        with allure.step("Initialize the authenticated API session"):
            csrf_response = self.get_csrf_cookie()
            if csrf_response.status_code not in (200, 204):
                raise RuntimeError(self.format_response_error("CSRF initialization failed.", csrf_response))

            token = self.get_xsrf_token()
            if not token:
                raise RuntimeError("XSRF-TOKEN cookie was not returned by /sanctum/csrf-cookie.")
            return token

    def login(self, email: str, password: str, token: str) -> requests.Response:
        login_url = self.build_url(self.login_endpoint)
        payload = {"email": email, "password": password}
        masked_payload = {"email": email, "password": "***"}
        headers = self.json_headers()
        headers["X-XSRF-TOKEN"] = token

        with allure.step("Submit the API login request"):
            self.logger.info("Login request: POST %s payload=%s", login_url, masked_payload)
            response = self.post(
                self.login_endpoint,
                json=payload,
                headers=headers,
            )
            self.logger.info("Login response: status=%s url=%s", response.status_code, response.url)
            return response

    def authenticate(self, email: str, password: str) -> requests.Response:
        with allure.step("Authenticate the API client with valid credentials"):
            token = self.get_csrf_token()
            return self.login(email=email, password=password, token=token)

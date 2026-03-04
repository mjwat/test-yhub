import logging
from typing import Any, Dict, Optional
from urllib.parse import unquote

import requests

from utils.url import build_url


class BaseApiClient:
    def __init__(
        self,
        base_url: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.session = session or requests.Session()
        self.logger = logging.getLogger(self.__class__.__module__)

    def build_url(self, path: str) -> str:
        return build_url(self.base_url, path)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        allow_redirects: bool = True,
    ) -> requests.Response:
        url = self.build_url(path)
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            files=files,
            headers=headers,
            allow_redirects=allow_redirects,
        )
        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", path, **kwargs)

    def get_xsrf_token(self) -> Optional[str]:
        token = self.session.cookies.get("XSRF-TOKEN")
        if token is None:
            return None
        return unquote(token)

    @staticmethod
    def json_headers() -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def xsrf_json_headers(self) -> Dict[str, str]:
        token = self.get_xsrf_token()
        headers = self.json_headers()
        headers["X-XSRF-TOKEN"] = token or ""
        return headers

    @staticmethod
    def format_response_error(prefix: str, response: requests.Response) -> str:
        return (
            f"{prefix} Status code: {response.status_code}. "
            f"URL: {response.request.url}. Body: {response.text[:500]}"
        )

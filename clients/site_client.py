import logging
from typing import Optional
from urllib.parse import unquote

import requests

from utils.url import build_url

logger = logging.getLogger(__name__)


class SiteClient:
    def __init__(
        self,
        base_url: str,
        site_create_page_endpoint: str,
        site_endpoint: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.site_create_page_endpoint = site_create_page_endpoint
        self.site_endpoint = site_endpoint
        self.session = session or requests.Session()

    def get_site_creation_page(self) -> requests.Response:
        page_url = build_url(self.base_url, self.site_create_page_endpoint)
        logger.info("Site creation page request: GET %s", page_url)
        response = self.session.get(url=page_url, allow_redirects=True)
        logger.info("Site creation page response: status=%s url=%s", response.status_code, response.url)
        return response

    def create_site_from_git_url(self, git_repo_url: str) -> requests.Response:
        create_url = build_url(self.base_url, self.site_endpoint)
        xsrf_token = self.session.cookies.get("XSRF-TOKEN")
        decoded_xsrf_token = unquote(xsrf_token) if xsrf_token else ""
        headers = {
            "X-XSRF-TOKEN": decoded_xsrf_token,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        logger.info("Site create (git) request: POST %s git_repo_url=%s", create_url, git_repo_url)
        response = self.session.post(
            url=create_url,
            json={"github_url": git_repo_url},
            headers=headers,
            allow_redirects=False,
        )
        logger.info("Site create (git) response: status=%s url=%s", response.status_code, response.url)
        return response

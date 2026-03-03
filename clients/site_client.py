import json
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

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

    def get_user_sites(self) -> List[Dict[str, Any]]:
        sites_url = build_url(self.base_url, self.site_endpoint)
        logger.info("Site list request: GET %s", sites_url)
        response = self.session.get(url=sites_url, allow_redirects=True)
        logger.info("Site list response: status=%s url=%s", response.status_code, response.url)

        if response.status_code != 200:
            raise RuntimeError(
                f"Expected status 200 from site list page, got {response.status_code}. "
                f"URL: {response.url}. Body: {response.text[:500]}"
            )

        soup = BeautifulSoup(response.text, "html.parser")
        app_div = soup.find("div", id="app")
        if app_div is None:
            raise RuntimeError("Could not find div#app in site list HTML response.")

        data_page = app_div.get("data-page")
        if not data_page:
            raise RuntimeError("div#app does not contain data-page attribute.")

        try:
            page_data = json.loads(data_page)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Failed to parse data-page attribute as JSON.") from exc

        sites_data = page_data.get("props", {}).get("sites", {}).get("data", [])
        if sites_data is None:
            sites_data = []
        if not isinstance(sites_data, list):
            raise RuntimeError("Expected props.sites.data to be a list in data-page JSON.")

        result: List[Dict[str, Any]] = []
        for site in sites_data:
            if not isinstance(site, dict):
                raise RuntimeError("Each site record in props.sites.data must be an object.")

            site_id = site.get("id")
            full_link = site.get("full_link")
            if site_id is None or full_link is None:
                raise RuntimeError("Site record is missing required fields: id/full_link.")

            result.append({
                "id": site_id,
                "full_link": full_link,
            })

        return result

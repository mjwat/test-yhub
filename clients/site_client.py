import json
from typing import Any, Dict, List, Optional

import requests
from bs4 import BeautifulSoup

from clients.base_api_client import BaseApiClient


class SiteClient(BaseApiClient):
    def __init__(
        self,
        base_url: str,
        site_create_page_endpoint: str,
        site_endpoint: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        super().__init__(base_url=base_url, session=session)
        self.site_create_page_endpoint = site_create_page_endpoint
        self.site_endpoint = site_endpoint

    def get_site_creation_page(self) -> requests.Response:
        page_url = self.build_url(self.site_create_page_endpoint)
        self.logger.info("Site creation page request: GET %s", page_url)
        response = self.get(self.site_create_page_endpoint, allow_redirects=True)
        self.logger.info("Site creation page response: status=%s url=%s", response.status_code, response.url)
        return response

    def create_site_from_git_url(self, git_repo_url: str) -> requests.Response:
        create_url = self.build_url(self.site_endpoint)
        headers = self.xsrf_json_headers()
        self.logger.info("Site create (git) request: POST %s git_repo_url=%s", create_url, git_repo_url)
        response = self.post(
            self.site_endpoint,
            json={"github_url": git_repo_url},
            headers=headers,
            allow_redirects=False,
        )
        self.logger.info("Site create (git) response: status=%s url=%s", response.status_code, response.url)
        return response

    def delete_site(self, site_id: Any) -> requests.Response:
        delete_path = f"{self.site_endpoint}/{site_id}"
        delete_url = self.build_url(delete_path)
        headers = self.xsrf_json_headers()
        self.logger.info("Site delete request: DELETE %s", delete_url)
        response = self.request(
            "DELETE",
            delete_path,
            headers=headers,
            allow_redirects=False,
        )
        self.logger.info("Site delete response: status=%s url=%s", response.status_code, response.url)
        return response

    def delete_all_sites(self) -> Dict[str, Any]:
        sites = self.get_user_sites()
        summary: Dict[str, Any] = {
            "total_found": len(sites),
            "deleted_ids": [],
            "failed": [],
        }

        for site in sites:
            site_id = site.get("id")
            try:
                response = self.delete_site(site_id)
            except Exception as exc:  # pragma: no cover - defensive utility path
                summary["failed"].append(
                    {
                        "id": site_id,
                        "error": str(exc),
                    }
                )
                continue

            if response.status_code in (200, 202, 204, 302):
                summary["deleted_ids"].append(site_id)
            else:
                summary["failed"].append(
                    {
                        "id": site_id,
                        "status_code": response.status_code,
                        "location": response.headers.get("Location", ""),
                    }
                )

        summary["deleted_count"] = len(summary["deleted_ids"])
        summary["failed_count"] = len(summary["failed"])
        return summary

    def get_user_sites(self) -> List[Dict[str, Any]]:
        sites_url = self.build_url(self.site_endpoint)
        self.logger.info("Site list request: GET %s", sites_url)
        response = self.get(self.site_endpoint, allow_redirects=True)
        self.logger.info("Site list response: status=%s url=%s", response.status_code, response.url)

        if response.status_code != 200:
            raise RuntimeError(self.format_response_error("Expected status 200 from site list page.", response))

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

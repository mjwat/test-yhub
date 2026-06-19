import json
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from clients.base_api_client import BaseApiClient

SITE_COUNT_LIMIT = 2


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

    def _extract_data_page(self, response: requests.Response) -> Dict[str, Any]:
        soup = BeautifulSoup(response.text, "html.parser")
        app_div = soup.find("div", id="app")
        if app_div is None:
            raise RuntimeError("Could not find div#app in HTML response.")

        data_page = app_div.get("data-page")
        if not data_page:
            raise RuntimeError("div#app does not contain data-page attribute.")

        try:
            return json.loads(data_page)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Failed to parse data-page attribute as JSON.") from exc

    def _extract_flash_message(self, response: requests.Response) -> str:
        data_page = self._extract_data_page(response)
        flash_message = data_page.get("props", {}).get("flash", {}).get("message")
        if flash_message is None:
            return ""
        if not isinstance(flash_message, str):
            raise RuntimeError("Expected props.flash.message to be a string when present.")
        return flash_message

    def create_site_from_git_url(self, git_repo_url: str) -> Dict[str, Any]:
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

        redirect_location = response.headers.get("Location", "")
        redirect_url = urljoin(create_url, redirect_location)

        redirect_response: Optional[requests.Response] = None
        flash_message = ""
        if redirect_location:
            redirect_response = self.session.get(redirect_url, allow_redirects=True)
            flash_message = self._extract_flash_message(redirect_response)
            self.logger.info(
                "Site create (git) redirect processed: redirect_status=%s final_url=%s flash_message=%s",
                redirect_response.status_code,
                redirect_response.url,
                flash_message,
            )
        else:
            self.logger.info("Site create (git) response has no redirect location header.")

        return {
            "initial_status_code": response.status_code,
            "redirect_location": redirect_location,
            "redirect_status_code": redirect_response.status_code if redirect_response is not None else None,
            "flash_message": flash_message,
            "final_url": redirect_response.url if redirect_response is not None else "",
        }

    def delete_site(self, site_id: Any) -> Dict[str, Any]:
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

        redirect_location = response.headers.get("Location", "")
        redirect_url = urljoin(delete_url, redirect_location)

        redirect_response: Optional[requests.Response] = None
        flash_message = ""
        if redirect_location:
            redirect_response = self.session.get(redirect_url, allow_redirects=True)
            flash_message = self._extract_flash_message(redirect_response)
            self.logger.info(
                "Site delete redirect processed: redirect_status=%s final_url=%s flash_message=%s",
                redirect_response.status_code,
                redirect_response.url,
                flash_message,
            )
        else:
            self.logger.info("Site delete response has no redirect location header.")

        return {
            "site_id": site_id,
            "initial_status_code": response.status_code,
            "redirect_location": redirect_location,
            "redirect_status_code": redirect_response.status_code if redirect_response is not None else None,
            "flash_message": flash_message,
            "final_url": redirect_response.url if redirect_response is not None else "",
        }

    def delete_all_sites(self) -> Dict[str, Any]:
        cleanup_pause_seconds = 20
        sites = self.get_user_sites()
        summary: Dict[str, Any] = {
            "total_found": len(sites),
            "deleted_ids": [],
            "failed": [],
        }

        for site in sites:
            site_id = site.get("id")
            try:
                delete_result = self.delete_site(site_id)
            except Exception as exc:  # pragma: no cover - defensive utility path
                summary["failed"].append(
                    {
                        "id": site_id,
                        "error": str(exc),
                    }
                )
                continue

            status_ok = delete_result.get("initial_status_code") == 302
            flash_ok = delete_result.get("flash_message") == "Site deleted successfully"
            if status_ok and flash_ok:
                summary["deleted_ids"].append(site_id)
            else:
                summary["failed"].append(
                    {
                        "id": site_id,
                        "initial_status_code": delete_result.get("initial_status_code"),
                        "redirect_location": delete_result.get("redirect_location", ""),
                        "redirect_status_code": delete_result.get("redirect_status_code"),
                        "flash_message": delete_result.get("flash_message", ""),
                        "final_url": delete_result.get("final_url", ""),
                    }
                )

        summary["deleted_count"] = len(summary["deleted_ids"])
        summary["failed_count"] = len(summary["failed"])
        if summary["deleted_count"] > 0 and summary["failed_count"] == 0:
            self.logger.info(
                "Deletion cleanup completed successfully. Waiting %s seconds for backend stabilization.",
                cleanup_pause_seconds,
            )
            time.sleep(cleanup_pause_seconds)
        return summary

    def get_user_sites(self) -> List[Dict[str, Any]]:
        sites_url = self.build_url(self.site_endpoint)
        self.logger.info("Site list request: GET %s", sites_url)
        response = self.get(self.site_endpoint, allow_redirects=True)
        self.logger.info("Site list response: status=%s url=%s", response.status_code, response.url)

        if response.status_code != 200:
            raise RuntimeError(self.format_response_error("Expected status 200 from site list page.", response))

        page_data = self._extract_data_page(response)

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

    def is_site_count_limit_reached(self) -> bool:
        current_site_count = len(self.get_user_sites())
        self.logger.info(
            "Site count limit check: current_site_count=%s limit=%s",
            current_site_count,
            SITE_COUNT_LIMIT,
        )
        return current_site_count >= SITE_COUNT_LIMIT

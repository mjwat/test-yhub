import logging
from typing import Optional

import requests

from utils.url import build_url

logger = logging.getLogger(__name__)


class SiteClient:
    def __init__(
        self,
        base_url: str,
        site_create_endpoint: str,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.site_create_endpoint = site_create_endpoint
        self.session = session or requests.Session()

    def get_site_creation_page(self) -> requests.Response:
        page_url = build_url(self.base_url, self.site_create_endpoint)
        logger.info("Site creation page request: GET %s", page_url)
        response = self.session.get(url=page_url, allow_redirects=True)
        logger.info("Site creation page response: status=%s url=%s", response.status_code, response.url)
        return response

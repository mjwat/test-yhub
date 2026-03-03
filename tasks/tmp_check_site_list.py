import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from clients.auth_client import AuthClient
from clients.site_client import SiteClient
from utils.config import get_env_config

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    config = get_env_config()

    auth_client = AuthClient(
        base_url=config["BASE_URL"],
        csrf_endpoint=config["CSRF_ENDPOINT"],
        login_endpoint=config["LOGIN_ENDPOINT"],
    )

    login_response = auth_client.authenticate(
        email=config["TEST_USER_EMAIL"],
        password=config["TEST_USER_PASSWORD"],
    )
    if login_response.status_code not in (200, 204):
        raise RuntimeError(
            f"Login failed. Status code: {login_response.status_code}. "
            f"URL: {login_response.request.url}. Body: {login_response.text[:500]}"
        )

    site_client = SiteClient(
        base_url=config["ADMIN_BASE_URL"],
        site_create_page_endpoint=config["SITE_CREATE_PAGE_ENDPOINT"],
        site_endpoint=config["SITE_ENDPOINT"],
        session=auth_client.session,
    )

    sites = site_client.get_user_sites()
    logger.info("Parsed %s sites from site list page.", len(sites))
    logger.info("Sites data:\n%s", json.dumps(sites, indent=2))


if __name__ == "__main__":
    main()

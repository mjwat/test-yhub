import json
import logging

import pytest

from clients.site_client import SiteClient

logger = logging.getLogger(__name__)


@pytest.mark.utility
def test_print_site_list(site_client: SiteClient) -> None:
    sites = site_client.get_user_sites()
    logger.info("Parsed sites:\n%s", json.dumps(sites, indent=2))


@pytest.mark.utility
def test_cleanup_all_sites(site_client: SiteClient) -> None:
    summary = site_client.delete_all_sites()
    logger.info("Site cleanup summary:\n%s", json.dumps(summary, indent=2))

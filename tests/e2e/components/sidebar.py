import re

from playwright.sync_api import Locator, Page


class Sidebar:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.sites_link: Locator = page.get_by_role("link", name=re.compile("sites", re.IGNORECASE))
        self.links_link: Locator = page.get_by_role("link", name=re.compile("links", re.IGNORECASE))
        self.logout_link: Locator = page.get_by_role("link", name=re.compile("logout", re.IGNORECASE))
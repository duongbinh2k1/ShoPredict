from playwright.sync_api import Page, Browser
from crawler.base.browser_manager import BrowserManager


class PageManager:
    def __init__(self, browser_manager: BrowserManager):
        self.browser_manager = browser_manager
        self.page: Page = None

    def new_page(self) -> Page:
        if self.browser_manager.browser:
            self.page = self.browser_manager.browser.new_page()
            return self.page
        return None

    def close_page(self):
        if self.page:
            self.page.close()

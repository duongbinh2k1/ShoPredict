from playwright.sync_api import sync_playwright, Browser


class BrowserManager:
    def __init__(self, playwright: sync_playwright):
        self.playwright = playwright
        self.browser: Browser = None

    def launch_browser(self):
        self.browser = self.playwright.chromium.launch()

    def close_browser(self):
        if self.browser:
            self.browser.close()
            self.playwright.stop()

from crawler.shopee.sp_page import SPPage
from crawler.base.browser_manager import BrowserManager
from crawler.base.page_manager import PageManager
from playwright.sync_api import sync_playwright

def crawl_man_clothes_shopee():
    with sync_playwright() as p:
        browser = BrowserManager(p)
        browser.launch_browser()

        page_manager = PageManager(browser)
        page = page_manager.new_page()

        sp_page = SPPage(page)
        sp_page.go_to_man_clothes()
        sp_page.get_all_product()


        browser.close_browser()

def crawl_woman_clothes_shopee():
    with sync_playwright() as p:
        browser = BrowserManager(p)
        browser.launch_browser()

        page_manager = PageManager(browser)
        page = page_manager.new_page()

        sp_page = SPPage(page)
        sp_page.go_to_man_clothes()
        sp_page.get_all_product()


        browser.close_browser()